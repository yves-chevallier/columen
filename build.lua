module = "columen"

sourcefiles  = {"columen.dtx","columen.ins"}
installfiles = {"columen.sty"}
typesetfiles = {"columen.dtx"}
typesetsuppfiles = {"columen.sty"}
tagfiles     = {"columen.dtx"} -- for versioning

checkengines = {"pdftex","xetex","luatex"}
typesetexe   = "pdflatex"

tdsroot = "texmf"
tdsdir  = "tex/latex/" .. module
