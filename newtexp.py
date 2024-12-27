#!/usr/bin/env python

import os
import argparse

# make a file with the contents
def makefile(filename, contents=''):
    f = open(filename,'w')
    f.write(contents)
    f.close()

latexmkrc = r'''
$texoption = ' %O -interaction=nonstopmode -file-line-error -synctex=1 %S';
$latex = 'uplatex'.$texoption;
$pdflatex = 'pdflatex'.$texoption;
$lualatex = 'lualatex'.$texoption;
$biber = 'biber %O --bblencoding=utf8 -u -U --output_safechars %B';
$bibtex = 'pbibtex %O %B';
$makeindex = 'mendex %O -o %D %S';
$dvipdf = 'dvipdfmx %O -o %D %S';
'''

uplatextemplate = r'''
\documentclass[paper=a4, fontsize=12pt, line_length=16cm, number_of_lines=33, baselineskip=23pt,dvipdfmx]{jlreq}

\usepackage{amsmath,amssymb}
\usepackage[bold,uplatex]{otf}
%% Fonts
\usepackage{tgtermes,tgheros,tgcursor}
\renewcommand{\bfdefault}{bx}
\usepackage[libertine]{newtxmath}
\usepackage{graphicx}

\begin{document}

\end{document}
'''

pdflatextemplate = r'''
\documentclass[12pt,a4paper]{article}
\usepackage[text={16.5cm,23cm},centering]{geometry}
\usepackage{amsmath}
\usepackage{amsthm}
%\usepackage{mathtools}
%\mathtoolsset{showonlyrefs,showmanualtags}
\usepackage[utf8]{inputenc}
\usepackage{tgtermes,tgheros,tgcursor}
\usepackage[varg]{newtxmath}
\usepackage{hyperref}
\hypersetup{%
 %setpagesize=false,
 %bookmarksnumbered=true,%
 %bookmarksopen=true,%
 colorlinks=true,%
 linkcolor=blue,
 citecolor=blue,
}
\usepackage{xspace}

\numberwithin{equation}{section}

\renewcommand{\baselinestretch}{1.2}

\newcommand{\pdv}[1]{\frac{\partial}{\partial #1}}
\newcommand{\del}{\partial}
\newcommand{\Ncal}{\mathcal{N}}
\newcommand{\Zb}{\mathbb{Z}}
\DeclareMathOperator*{\Tr}{\mathrm{Tr}}

\begin{document}
\begin{center}
  %% Preprint number
  \begin{flushright}
    OU-HET xxxx
  \end{flushright}
  \vspace{8ex}
  %% Title
  {\Large \bfseries \boldmath Supersymmetric quantum field theory with exotic symmetry in $3+1$ dimensions and fermionic fracton phases}\\
  \vspace{4ex}
  % Author
  {\Large Satoshi Yamaguchi}\\
  \vspace{2ex}
  {\itshape Department of Physics, Graduate School of Science, %affiliation
  \\
  Osaka University, Toyonaka, Osaka 560-0043, Japan}\\
  \vspace{1ex}
  \begin{abstract}
    We propose a supersymmetric quantum field theory with exotic symmetry related to fracton phases.  We use superfield formalism and write down the action of a supersymmetric version of the $\varphi$ theory in $3+1$ dimensions.  It contains a large number of ground states due to the fermionic higher pole subsystem symmetry.  Its residual entropy is proportional to the area instead of the volume.  This theory has a self-duality similar to that of the $\varphi$ theory.  We also write down the action of a supersymmetric version of a tensor gauge theory, and discuss BPS fractons.
  \end{abstract}
\end{center}

\vspace{4ex}
\section{Introduction and summary}


\subsection*{Acknowledgement}

\bibliographystyle{utphys}
\bibliography{ref}
\end{document}
'''

gitignore = r'''
*.aux
*.dvi
*.log
*.out
*.toc
*.synctex.gz
*.fdb_latexmk
*.bbl
*.blg
*.fls
'''

# コマンドラインパーズ
parser = argparse.ArgumentParser(description='Make new latex project')
parser.add_argument('projectname', type=str, help='Make the directory of this name and other files in it.')
parser.add_argument('--eng', '-e', action='store_true', help='Use English if specified. Otherwise use Japanese.')
args = parser.parse_args()
projectname = args.projectname  #プロジェクトの名前
ifeng = args.eng  #英語バージョンかどうか

# ディレクトリを作る。
os.mkdir(projectname)

# texファイルを書く
template = uplatextemplate
if ifeng:
    template = pdflatextemplate
makefile(projectname+'/'+projectname+'.tex', template)

# latexmkrcを書く
pdfmode = '3'

if ifeng:
    pdfmode = '1'
pdfmodestr = r'$pdf_mode = ' + pdfmode + ';\n'
makefile(projectname+'/'+'latexmkrc', latexmkrc + pdfmodestr)

# .gitignoreを書く
pdffile = projectname + '.pdf'
makefile(projectname+'/'+'.gitignore',  gitignore + pdffile)
