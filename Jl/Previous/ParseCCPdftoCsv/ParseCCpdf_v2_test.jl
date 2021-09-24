using PDFIO
using CSVFiles
using DataFrames
using CSV
using Gumbo
using Cascadia
using Dates
import Gumbo.text
using Statistics
using Test

cd("C:/Users/jasonjia/Dropbox/ConferenceCall/Output")
filename="20201001-20201004_1"

function parseHtmlXlsToDf(filename)
    print(string("parseHtmlXlsToDf: ", " | "))
    try
        list_html_raw=read(filename,String)
        list_html = parsehtml(String(list_html_raw))
        dflist=DataFrame(PPV=String[],TOC=String[],Title=String[],Subtitle=String[],Date=Dates.Date[],Pages=Int[],Price=String[],Contributor=String[],
                Analyst=[],Language=[],Report=Int[],Collection=[])
        tr=eachmatch(sel"tr", list_html.root)
        nrow=size(tr)[1]-1
        for i=2:(nrow+1)
            td=eachmatch(sel"td", tr[i])
            date_row=Date(text(td[5][1]),"mm/dd/yy")
            date_row=Year(date_row)<Year(1900) ? date_row+Year(2000) : date_row
            row=[text(td[1][1]),text(td[2][1]),text(td[3][1]),text(td[4][1]),date_row,parse(Int,text(td[6][1])),text(td[7][1]),text(td[8][1]),text(td[9][1]),
                    text(td[11][1]),parse(Int,text(td[12][1])),text(td[13][1])]
            push!(dflist,row)
        end
        return  dflist
    catch e
        println(string(e)[1:50])
    end
end

dflist=parseHtmlXlsToDf("ListTest/$filename.xls")

# dflist=parseHtmlXlsToDf("ListTest/$filename.xls")
list_html_raw=read("ListTest/$filename.xls",String)
list_html = parsehtml(String(list_html_raw))
dflist=DataFrame(PPV=String[],TOC=String[],Title=String[],Subtitle=String[],Date=Dates.Date[],Pages=Int[],Price=String[],Contributor=String[],
        Analyst=[],Language=[],Report=Int[],Collection=[])
tr=eachmatch(sel"tr", list_html.root)
nrow=size(tr)[1]-1
for i=2:(nrow+1)
    td=eachmatch(sel"td", tr[i])
    date_row=Date(text(td[5][1]),"mm/dd/yy")
    date_row=Year(date_row)<Year(1900) ? date_row+Year(2000) : date_row
    row=[text(td[1][1]),text(td[2][1]),text(td[3][1]),text(td[4][1]),date_row,parse(Int,text(td[6][1])),text(td[7][1]),text(td[8][1]),text(td[9][1]),
            text(td[11][1]),parse(Int,text(td[12][1])),text(td[13][1])]
    push!(dflist,row)
end
dflist
print(dflist)
dflist[!,:Call].=""

#back to parseCalls
doc_pdf = pdDocOpen("CallScriptsTest/$filename.pdf")
doc_text=String(read("CallScriptsTest/$filename.txt"))
doc=split(doc_text,"\f")

function getPageContents(doc)
    print(string("getPageContents", " | "))
    try
    i=1
    content=""
    while true
        try
            page=getPage(doc,i)
            findfirst("Table of Contents",page)[1]
            content=string(content," \n ",page)
            i+=1
        catch
            break
        end
    end
    return content, (i-1)
catch e
    println(string(e)[1:50])
end
end

function getPage(doc,page_n)
    print(string(page_n,"--"))
    try
        page = pdDocGetPage(doc, page_n)
        io = IOBuffer()
        pdPageExtractText(io, page)
        page_str=String(take!(io))
    catch
        page_str=""
    end
end

content, pn = getPageContents(doc_pdf)
print(content)
print(pn)

row1 = eachrow(dflist)[1]
rowend = eachrow(dflist)[end]
firmname=row.Title
analyst=row.Analyst
report_number=row.Report
page_size=row.Pages
print(string(firmname, "-", analyst, "-", report_number, "-", page_size))

##
# to another function
function getFirmPageNumber(content,report_n::Int)
    println(".")
    print(string("getFirmPageNumber: ",report_n," | "))
    try
    l=findfirst(string(report_n),content)[end]
    e=findnext("-",content,l+70)[1]
    #return parse(Int,content[e-5:e-1])
    return parse(Int,content[e-4:e-1])
catch e
    return 1
end
end

page_n=getFirmPageNumber(content,report_number)

println(".")
print(string("getFirmPageNumber: ",report_number," | "))
l=findfirst(string(report_number),content)[end]
e=findnext("-",content,l+70)[1]
return parse(Int,content[e-4:e-1])

##
function getFirmCC_t3(doc,page_s,page_e)
    print(string("getFirmCC: ",page_s,", ",page_e, " | "))
    try
    call=""
    for i=page_s+1:page_e
        # println("page-",i)
        page=getPage(doc,i)
        if page!=""
            page=cutHeader(page,false)
            if length(page)<700
                break
            end
            page=cutBottom(page)
            call=string(call," \n ",page)
        else
            break
        end
    end
    call=cutDisclaimer(call)
    return call
catch e
    println(string(e)[1:50])
    return ""
end
end

function getPage(doc::Vector,page_n)
    print(string(page_n,"-"))
    try
        return doc[page_n]
    catch e
        println(string(e)[1:50])
    end
end

function cutHeader(page,lastpage=false)
    # println("cutHeader")
    try
    if !isnothing(findfirst("PRELIMINARY",page))
        p=findfirst("PRELIMINARY",page)[end]
        l=findnext("\n\n",page,p+10)[end]
        return page[l+1:end]
    else
        l=findfirst("\n\n",page)[end]
        ll=0
        if lastpage
            if !isnothing(findfirst("\n\n",page[nextind(page,l+10):nextind(page,l+150)]))
                ll=l
                l=findfirst("\n\n",page[nextind(page,l+10):nextind(page,l+150)])[end]+10
            end
            return page[ll+l:end]
        else
            return page[l+1:end]
        end

    end
catch e
    println(string(e)[1:50])
end
end


function cutBottom(page)
    # println("cutBottom")
    page=replace(page,"\n\n\n\n\n"=>"")
    page=replace(page,"\n\n\n\n"=>"")
    page=replace(page,"\n\n\n"=>"\n\n")
    try
        if !isnothing(findfirst(r"\d{1,3}\n{0,}refinitiv streetevents \|",uppercase(page[prevind(page, lastindex(page),700):end])))
            l=findfirst(r"\d{1,3}\n{0,}refinitiv streetevents \|",uppercase(page[prevind(page, lastindex(page),700):end]))[1]
            # elseif !isnothing(findfirst(r"REFINITIV STREETEVENTS \|",uppercase(page[prevind(page, lastindex(page),700):end])))
            #    l=findfirst(r"REFINITIV STREETEVENTS \|",uppercase(page[prevind(page, lastindex(page),700):end]))[1]
        else
            l=0
        end
        return  page[1:prevind(page, lastindex(page),700-l+3)]
        #return page[1:end-700+l-3]
    catch e
        println("cutBottom_catch")
        println(string(e)[1:50])
            return page
    end
end

function cutDisclaimer(page)
    try
    if !isnothing(findfirst("DISCLAIMER\n",page))
            l=findfirst("DISCLAIMER\n",page)[1]
    elseif  !isnothing(findfirst("DISCLAIMER:",page))
            l=findfirst("DISCLAIMER:",page)[1]
    elseif  !isnothing(findfirst("all products and services provided by fdfn",lowercase(page)))
            l=findfirst("all products and services provided by fdfn",lowercase(page))[1]
    else
            l=lastindex(page)+1
    end
    return page[1:l-1]
catch e
    println(string(e)[1:50])
end
end

call=getFirmCC_t3(doc,page_n,page_n+page_size-1)

# Start of function getFirmCC_t3(doc,page_n,page_n+page_size-1)
page_s = page_n
page_e = page_n+page_size-1

print(string("getFirmCC: ",page_s,", ",page_e, " | "))
call=""

for i=page_s+1:page_e
# function: page = getPage(doc,i)
    print(string(i,"-"))
    page = doc[page_n]
    print(page)
end

i=page_s+1
page=getPage(doc,i)
page
println("---------------------------------------------")
page=cutHeader(page,false)
page
println("---------------------------------------------")
page=cutBottom(page)pag
print(page)
println("---------------------------------------------")
call=string(call," \n ",page)
print(call)
println("---------------------------------------------")
call=cutDisclaimer(call)
print(call)
println(".")

row[:Call]=call

call2=""
i=page_e
page2=getPage(doc,i)
print(page2)
println("---------------------------------------------")
page2=cutHeader(page2,false)
print(page2)
println("---------------------------------------------")
page2=cutBottom(page2)
print(page2)
println("---------------------------------------------")
call2=string(call2," \n ",page2)
print(call2)
println("---------------------------------------------")
call2=cutDisclaimer(call2)
print(call2)
println(".")

rowend[:Call]=call2

print(row)
pdDocClose(doc_pdf)
print(dflist)

# and typically, flows like these will
