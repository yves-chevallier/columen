module = "columnspread"

sourcefiles  = {"columnspread.dtx","columnspread.ins"}
installfiles = {"columnspread.sty"}
typesetfiles = {"columnspread.dtx"}
tagfiles     = {"columnspread.dtx"} -- for versioning

checkengines = {"xetex","luatex"}
typesetexe   = "lualatex"

tdsroot = "texmf"
tdsdir  = "tex/latex/" .. module
