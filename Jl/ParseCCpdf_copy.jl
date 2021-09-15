# ```This code parse text Concference Calls (CC) to CSV Data Frame ```
# ```Code uses two files: 1) *.XLS file with a list of CC per file and 2) *.txt file, which was converted from pdf file ```
# ```Code use information from XLS file about type of Anaylist to parse CC in different ways ```


using PDFIO
using CSVFiles
using DataFrames
using CSV
using Gumbo
using Cascadia
using Dates
import Gumbo.text
using Statistics

``` read list of firm per pdf documents ```
function parseHtmlXlsToDf(filename)
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

``` get page from the document ```
function getPage(doc::Vector,page_n)
    try
        return doc[page_n]
    catch e
        println(string(e)[1:50])
    end
end


function getPage(doc,page_n)
    try
        page = pdDocGetPage(doc, page_n)
        io = IOBuffer()
        pdPageExtractText(io, page)
        page_str=String(take!(io))
    catch
        page_str=""
    end
end


``` get contents of the pdf documnet```
function getPageContents(doc)
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


``` get from the content the first page number of the CCall firm by name or by Rpt number```
``` we use report number, since the firm can have several report for a documents ```
function getFirmPageNumber(content,report_n::Int)
    try
    l=findfirst(string(report_n),content)[end]
    e=findnext("-",content,l+70)[1]
    #return parse(Int,content[e-5:e-1])
    return parse(Int,content[e-4:e-1])
catch e
    return 1
end
end

``` 1st type of CCall```
function cutHeader(page,lastpage=false)
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
    try
        if !isnothing(findfirst("refinitiv streetevents",lowercase(page[prevind(page, lastindex(page),700):end])))
            l=findfirst("refinitiv streetevents",lowercase(page[prevind(page, lastindex(page),700):end]))[1]
        elseif !isnothing(findfirst("streetevents@thomson.com",lowercase(page[prevind(page, lastindex(page),700):end])))
            l=findfirst("streetevents@thomson.com",lowercase(page[prevind(page, lastindex(page),700):end]))[1]
        else
            l=0
        end
        return  page[1:prevind(page, lastindex(page),700-l+3)]
        #return page[1:end-700+l-3]
    catch
        println("cutBotton_catch")
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


function IsTwoColumns(page)
    lines=split(page,"\n")
    sc_s=zeros(length(lines))
    sc_e=zeros(length(lines))
    for i=1:length(lines)
            sc_s[i],sc_e[i]=findColumn(lines[i])
    end
    sc_mean=mean(sc_s)
    sc_v=var(sc_s)^.5
    if (sc_mean<70 || sc_mean>30) & (sc_v<40)
        return  true
    else
        return false
    end
end

function getFirmCC_t1(doc,page_s,page_e)
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

            if IsTwoColumns(page)
                page=twoColumsToText(page)
            end
            # if i==page_e
            #     page=cutDisclaimer(page)
            # end
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

``` end 1st type ```
``` 2nd type ```

function fistPage_t2(page)

    l=0
    try
        # l=findfirst("THE OPERATOR:",page)[1]
        d=findfirst("Disclaimer:",page)[end]
        l=findnext("\n\n",page,d)[end]+3
    catch
    end
    if l==0
        return ""
    else
        return page[l-1:end]
    end
end

function cutHeaderFooter_t2_1(page)
    try
    f=findfirst("fair disclosure financial network",lowercase(page))[1]
    return page[1:f-1]
catch e
    println(string(e)[1:50])
end
end


function cutHeaderFooter_t2_2(page)
    try
    if lastindex(page)==0
        return page
    else
        h=1
        try
             h=findfirst("\n\n\n",page)[1]
             if h>400
                 h=findfirst("\n\n",page)[1]
             end
        catch
        end

        if !isnothing(findfirst("fair disclosure financial network",lowercase(page[prevind(page, lastindex(page),300):end])))
            f=findfirst("fair disclosure financial network",lowercase(page[prevind(page, lastindex(page),300):end]))[1]
            return page[h:prevind(page, lastindex(page),400-f+4)]
        else
            return page[h:end]
        end
    end
catch e
    println(string(e)[1:50])
end
end

```given line, looking for a second conlumn start ```

function findColumn(line)
    try
        if length(line)>0
            if length(line)>55
                if length(strip(line))<50
                    return (length(line)- length(strip(line))),(length(line)- length(strip(line))+1)
                 else
                    d=10
                     while isnothing(findfirst(" "^d,line[nextind(line,44):end]))
                         d=d-1
                     end
                     if d>2
                         sc=findfirst(" "^d,line[nextind(line,44):end])
                         return nextind(line,43+sc[1]), nextind(line,43+sc[end])
                     else
                         return lastindex(line) , 0
                     end
                end
             else
                 return lastindex(line) , 0
             end
         else
             return 0,0
         end
     catch e
        println(string(e)[1:50])
     end
end


function twoColumsToText(page,disclaimer=false)
    try
    lines=split(page,"\n")
    column1=""
    column2=""
    for i=1:length(lines)
            # println(i)
            sc_s,sc_e =findColumn(lines[i])
            line1=strip(lines[i][1:sc_s])
            if length(line1)>0
                  column1=string(column1,"\n",line1)
            end

            if sc_e!=0
                line2=strip(lines[i][sc_e:end])
                if length(line2)>0
                       column2=string(column2,"\n",line2)
                end
            end
    end
    if disclaimer==true
        try
            if !isnothing(findfirst("THE OPERATOR",column1))
                f=findfirst("THE OPERATOR",column1)[1]-1
            elseif !isnothing(findfirst("deemed to be rendering investment advice",column1))
                    f=findfirst("deemed to be rendering investment advice",column1)[end]+1
            end
            column1=column1[nextind(column1,f) : end]
        catch
        end
    end

    return  string(column1,column2)
catch e
    println(string(e)[1:40])
end
end


function getFirmCC_t2(doc,page_s,page_e) #type 2, Analyst==FDFN.COM
    try
    call=""
    type=1
    for i=page_s:page_e
         # println("page-",i)
        page=getPage(doc,i)
        #first page
        if i==page_s
            page=fistPage_t2(page)
            # if page is empty => second type
            if page==""
                type=2
            end
        end
        if type==1
            page=cutHeaderFooter_t2_1(page)
        elseif type==2
                page=cutHeaderFooter_t2_2(page)
                disclaimer=false
                if i==(page_s+1)
                    disclaimer=true
                end
                    page=twoColumsToText(page,disclaimer)
        end
         call=string(call," \n ",page)
    end
    call = cutDisclaimer(call)
    return call
catch e
    println(string(e)[1:50])
    return ""
end
end

function isFDFN(doc,page_n)
    page=getPage(doc,page_n)
    return !isnothing(findfirst("fair disclosure financial network",lowercase(page)))
end

# ``` Parse file```
function parseCalls(filename)
    try
    #get list of CC
    dflist=parseHtmlXlsToDf("$filename.xls")
    dflist[!,:Call].=""

    #doc = pdDocOpen("$filename.pdf")
    doc_pdf = pdDocOpen("$filename.pdf")
    doc_text=String(read("$filename.txt"))
    doc=split(doc_text,"\f")
    content, pn = getPageContents(doc_pdf)
    # row=dflist[50,:]
    if size(dflist)[1]!=1
        for row in eachrow(dflist)
            try
                #println(row.Title)
                firmname=row.Title
                analyst=row.Analyst
                report_number=row.Report
                page_size=row.Pages
                page_n=getFirmPageNumber(content,report_number)
                if page_n!=1
                    if (analyst=="FDFN.COM") || (isFDFN(doc,page_n+1))
                        call=getFirmCC_t2(doc,page_n,page_n+page_size-1)
                    else
                        # call=getFirmCC_t1(doc_pdf,page_n,page_n+page_size-1)
                        call=getFirmCC_t1(doc,page_n,page_n+page_size-1)
                    end
                    row[:Call]=call
                else
                    global dfBadFile
                    push!(dfBadFile,[filename,row.Title])
                    CSV.write("BadList.csv",dfBadFile)
                end
            catch e
                println("Row Error:-",e)
                row[:Call]=""
            end
        end
    else
        row=dflist[1,:]
        try
            #println(row.Title)
            analyst=row.Analyst
            page_size=row.Pages
            if (analyst=="FDFN.COM") || (isFDFN(doc,2))
                call=getFirmCC_t2(doc,1,page_size)
            else
                call=getFirmCC_t1(doc,1,page_size)
            end
                row[:Call]=call
        catch e
            println("Row Error:-",e)
            row[:Call]=""
        end
    end
    pdDocClose(doc_pdf)
    return dflist
catch e
    println(e)
    try
        pdDocClose(doc_pdf)
    catch
    end
end
end

# ```parse all file from the currrent  ```
function main()
    files=readdir()
    for file in files
        if file[end-2:end]=="xls"
            try
                filename=file[1:end-4]
                println(file)
                @time dfCalls=parseCalls(filename)
                CSV.write("$filename.csv",dfCalls)
            catch e
                println(e)
            end
        end
    end
end


# ACTUAL CODE STARTS

println("start Parse CC pdf")
global dfBadFile=DataFrame(filename=String[],Title=String[])

# Overall structure: -> main
try
    # Sixun's comment, N/A: cd("..//..//..//..//project//EC_Mercury//final_sup")
    cd("/Users/jasonjia/ConferenceCall/Misc/Trial")
    @time main()
    CSV.write("BadList.csv",dfBadFile)
    # filename="20030311-20030314_1"
    # df=parseCalls(filename)
catch e
    println(e)
end
CSV.write("BadList.csv",dfBadFile)
println("Finish Parse CC pdf")
