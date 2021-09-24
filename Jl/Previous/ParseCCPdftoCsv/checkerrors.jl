# Idea: If you find "The application encountered an internal error.", record the file name into a csv and save it.
# To-do: What if xls is missing? What if pdf is missing? Cross-check file names...
# To-do: download those next in line.

using PDFIO
using CSVFiles
using DataFrames
using CSV
using Gumbo
import Gumbo.text


function errorxls(file)
    filename=file[1:end-4]
    list_html_raw=read(file,String)
    if !isnothing(findfirst("The application encountered an internal error",list_html_raw))
        error = "yes"
    else
        error = "no"
    end
    push!(dfErrorXls,[filename, error])
    CSV.write("Errorxlsfiles.csv",dfErrorXls)
end

cd("C:/Users/jasonjia/Dropbox/ConferenceCall/Output/Xls")
files=readdir()

dfErrorXls=DataFrame(filename=String[],error=String[])

for file in files
    if file[end-2:end]=="xls"
        errorxls(file)
    end
end

