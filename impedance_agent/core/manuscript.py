"""Workspace manuscript adapter for richinex PlotManager.

Adds raw multi-spectrum overlays and descriptive finite-amplitude C-AFM support.
This is a local extension, not upstream C-AFM fitting or LLM analysis.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapezoid
from .plotting import PlotManager
from .models import AnalysisResult


class ManuscriptPlotManager(PlotManager):
    SIZE = (8, 6)
    AX_RECT = (.12, .36, .84, .49)
    DPI = 600
    EIS_STYLE = 'All EIS curves: dashed lines with points; circles: initial/forward; squares: reverse/after sweep.'

    @staticmethod
    def _frame(title):
        plt.rcParams.update({'font.family':'Arial','font.size':10,'axes.labelsize':10,
            'xtick.labelsize':9,'ytick.labelsize':9,'legend.fontsize':8.5,
            'pdf.fonttype':42,'svg.fonttype':'none'})
        fig=plt.figure(figsize=ManuscriptPlotManager.SIZE)
        ax=fig.add_axes(ManuscriptPlotManager.AX_RECT)
        fig.text(.5,.95,title,ha='center',va='top',fontsize=11)
        ax.grid(alpha=.18,linestyle='--',lw=.55)
        ax.tick_params(direction='in',top=True,right=True)
        return fig,ax

    @staticmethod
    def _export(fig,ax,path,caption,ncol):
        handles,labels=ax.get_legend_handles_labels()
        if ax.get_legend() is not None: ax.get_legend().remove()
        fig.legend(handles,labels,loc='upper center',bbox_to_anchor=(.5,.225),
                   ncol=ncol,frameon=False,columnspacing=1.1,handlelength=2.7,fontsize=8.5)
        fig.text(.5,.028,caption,ha='center',fontsize=8)
        path=Path(path)
        for ext in ['png','pdf','svg']:
            fig.savefig(path.with_suffix('.'+ext),dpi=ManuscriptPlotManager.DPI)
        plt.close(fig)

    @staticmethod
    def nyquist(curves,path,title,axis_limits=None):
        """Draw measured data through the native Nyquist method, never fitted substitutes."""
        fig,ax=ManuscriptPlotManager._frame(title)
        for curve in curves:
            previous=len(ax.lines)
            PlotManager._plot_nyquist(AnalysisResult(),ax,experimental_data=curve['data'],unit_scale=1e6)
            line=ax.lines[previous]
            reverse=curve.get('saved_id') in [5,6,7,11,12,13]
            line.set(color=curve['color'],linestyle='--',marker='s' if reverse else 'o',markersize=2.3,
                markevery=10,linewidth=1.4,label=curve['label'],markeredgewidth=.55)
        ax.set_title('')
        ax.set(xlabel='Re(Z) (MΩ)',ylabel='−Im(Z) (MΩ)')
        if axis_limits is None:
            x=np.concatenate([c['data'].real for c in curves])/1e6
            y=np.concatenate([-c['data'].imaginary for c in curves])/1e6
            dx=float(x.max()-min(x.min(),0)); dy=float(y.max()-min(y.min(),0))
            lo_x=min(float(x.min()),0)-.035*dx
            hi_x=float(x.max())+.035*dx
            lo_y=min(float(y.min()),0)-.035*max(dy,dx*.2)
            height_over_width=ManuscriptPlotManager.SIZE[1]*ManuscriptPlotManager.AX_RECT[3]/(
                ManuscriptPlotManager.SIZE[0]*ManuscriptPlotManager.AX_RECT[2])
            hi_y=max(float(y.max())+.035*dy,lo_y+(hi_x-lo_x)*height_over_width)
            hi_x=max(hi_x,lo_x+(hi_y-lo_y)/height_over_width)
            axis_limits={'x_MOhm':[lo_x,hi_x],'minus_Im_MOhm':[lo_y,hi_y]}
        ax.set_xlim(axis_limits['x_MOhm']); ax.set_ylim(axis_limits['minus_Im_MOhm'])
        ax.set_aspect('equal',adjustable='box')
        for c in curves:
            x=c['data'].real/1e6; y=-c['data'].imaginary/1e6
            assert np.all((x>=ax.get_xlim()[0])&(x<=ax.get_xlim()[1])&(y>=ax.get_ylim()[0])&(y<=ax.get_ylim()[1]))
        ManuscriptPlotManager._export(fig,ax,path,
            '40 Hz–110 MHz · AC 20 mA nominal · circles: initial/forward; squares: reverse/after sweep',4 if len(curves)>3 else 3)
        return axis_limits

    @staticmethod
    def iv(loops,path,title):
        """C-AFM adapter: plot raw V/nA branches and calculate descriptive loop areas only."""
        fig,ax=ManuscriptPlotManager._frame(title)
        metrics=[]
        for i,loop in enumerate(loops):
            a=loop['values']; color=plt.get_cmap('tab10')(i)
            ax.plot(a[:,0],a[:,1],color=color,lw=1.4,label=f"{loop['rate']:g} V/s (curve {loop['curve']})")
            ax.plot(a[::-1,0],a[::-1,2],color=color,ls='--',lw=1.4)
            metrics.append({'rate_V_per_s':loop['rate'],'curve':loop['curve'],
                'absolute_branch_separation_nA_V':float(trapezoid(abs(a[:,2]-a[:,1]),a[:,0]))})
        currents=np.concatenate([l['values'][:,1:].ravel() for l in loops])
        span=float(currents.max()-currents.min())
        ylim=[float(currents.min())-.04*span,float(currents.max())+.04*span]
        ax.set(xlabel='Voltage (V)',ylabel='Current (nA)',xlim=(-.1,10.1),ylim=ylim)
        ax.axhline(0,color='gray',lw=.55)
        ManuscriptPlotManager._export(fig,ax,path,
            'C-AFM · 0–10 V · solid: forward; dashed: reverse · unchanged selected raw curves',3)
        return {'axis_limits':{'voltage_V':[-.1,10.1],'current_nA':ylim},'measured_descriptors':metrics}
