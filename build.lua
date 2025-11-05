module = "columnspread"

sourcefiles  = {"columnspread.dtx","columnspread.ins"}
installfiles = {"columnspread.sty"}
typesetfiles = {"columnspread.dtx"}
typesetsuppfiles = {"columnspread.sty"}
tagfiles     = {"columnspread.dtx"} -- for versioning

checkengines = {"pdftex","xetex","luatex"}
typesetexe   = "pdflatex"

tdsroot = "texmf"
tdsdir  = "tex/latex/" .. module
