
``` File has to run by Julia Language ```
 ```     Parse CC datalist to match firm name to compustat gvkey and country ```
 ```     Three source are using: 1) Hassan dataset 2) compustat capital IQ companies dataset 3) compustat capital IQ ticker ```
 ```     For unmatched firm's name, string distance comparison is using. ```
```     Execute all code with function definiton before main code ```
```     Set auxilary path foder (the foder is coming with this file) ```
```     Set CC CSV folder ```
```     Run main code ```
```     Resuls is CC_list.csv file, in the CSV folder ```

using CSV
using DataFrames
using StringDistances

function getTicker(str) #``` parse tiker ```
    try
        f=findfirst(" - ",str)[1]
        p=findfirst(".",str[1:f-1])[1]
        return str[1:p-1]
    catch
        return ""
    end
end

function deleteCorpWords(fname) #``` delete common words```
    words=["group","plc","ltd","limited","ag","corp","corporation","Incorporation","laboratories","labs","the",
                        "holdings","oyj","inc","conference call","conference","co",
                        "company","trust","investment","investments","sln","sa"]
    for w in words
        fname=replace(fname,Regex("\\b$w\\b") => " ")
    end
    return strip(fname)
end


function prepareName(fname) #""" prepare name for matching """
    fname=lowercase(fname)
    fname=replace(fname,r"\((.*)\)"=>"")
    try
        f=findfirst("event transcript of",fname)[end]
        fname=fname[f+1:end]
    catch
    end
    try
        f=findfirst("event brief of",fname)[end]
        fname=fname[f+1:end]
    catch
    end
    fname=replace(fname,r"[.,'#-/0-9]"=>"")
    return deleteCorpWords(fname)
end

function getGVkeyH(fname)
    try
        return gvkey_dict_h[prepareName(fname)]
    catch
        return 0
    end
end

function getGVkeyC(fname)
    try
        return gvkey_dict_c[prepareName(fname)]
    catch
        return 0
    end
end

function getGVKey_ticker(ticker)
    try
        return ticker_gvkey_uniq[ticker]
    catch
        return 0
    end
end

function GuesNameTicker!(dfCC) #```lookf through set of company names by tikers. (some tickers has several names) ```
    dfCC[!,:prob].=1.
    dfCC[!,:gues_by_dticker].=0
    dfCC[!,:gues_name].=""
    for r in eachrow(dfCC)
        if r.gvkey==0
            # println(r.ticker)
            possible_compname= dfCompT[dfCompT.tickersymbol.==r.ticker,:] #set of possible company names
            if size(possible_compname)[1]>1
                prob=0
                best_match=""
                gvkey_match=0
                for pn in eachrow(possible_compname)
                    p=compare(prepareName(pn.companyname),prepareName(r.Title),Jaro())
                    if p>prob
                         prob=p
                         best_match=pn.companyname
                         gvkey_match=pn.gvkey
                    end
                end
                if prob>0.7
                    r.prob=prob
                    r.gues_name=best_match
                    r.gvkey=gvkey_match
                    r.gues_by_dticker=1
                end
            end
        end
    end
end


function GuesName!(dfCC) #""" mactch companies name by the best matched"""

    # dfCC[!,:prob].=1.
    # dfCC[!,:gues_name].=""

    for r in eachrow(dfCC)
        if r.gvkey==0
            fname=prepareName(r.Title)
            best_match=firm_names[1]
            gvkey_match=gvkey_dict_h[best_match]
            prob=compare(fname, best_match, Jaro())
            for f in firm_names[2:end]
                p=compare(fname, f, Jaro())
                if p>prob
                  prob=p
                  best_match=f
                  gvkey_match = haskey(gvkey_dict_h,best_match) ? gvkey_dict_h[best_match] : gvkey_dict_c[best_match]
                end
            end
            r.prob=prob
            r.gvkey=gvkey_match
            r.gues_name=best_match
        end
    end
end

function MergeGvkey!(dfCC)# """ create the main gvkey based on three keys: hassan, compustat, tickers """
    dfCC[!,:gvkey].=0
    for r in eachrow(dfCC)
        if !((r.gvkey_t.==0) .& (r.gvkey_h.==0) .& (r.gvkey_c.==0))
            r.gvkey=r.gvkey_c
            if r.gvkey==0
                r.gvkey=r.gvkey_h
                if r.gvkey==0
                    r.gvkey=r.gvkey_t
                end
            end
        end
    end
end


function  matchFile(filename)
    #read Call csv file
    try
        dfCC=CSV.read("$filename.csv",DataFrame,copycols=true)

        #parse ticker from SubTitile
        dfCC[!,:ticker]=getTicker.(dfCC.Subtitle)
        #match three sources gvkeys
        dfCC[!,:gvkey_t].= getGVKey_ticker.(dfCC[:,:ticker])
        dfCC[!,:gvkey_h]=getGVkeyH.(dfCC.Title)
        dfCC[!,:gvkey_c]=getGVkeyC.(dfCC.Title)

        #Merge into one main gvkey
        MergeGvkey!(dfCC)
        #match firms without gvkey
        GuesNameTicker!(dfCC)
        GuesName!(dfCC)
        #println(dfCC[:,[:gvkey_c,:gvkey_h,:gvkey_t,:gvkey,:prob,:Title,:gues_name]])

        dfCC=join(dfCC,dfCompGvkeyUniqu[:,[:gvkey,:countryid,:country]], on = :gvkey, kind = :inner)
        dfCC[!,:filename].=filename
        select!(dfCC,Not(:Call))
        return dfCC
    catch
    end
end



function DoFolder()
    dfList=DataFrame()
    files=readdir()
    for file in files
        if file[end-2:end]=="csv"
            println(file)
            try
                dfCC=matchFile(file[1:end-4])
                # if ismissing(dfCC[1,:Call])
                #     dfCC[!,:Call].=""
                # end
                append!(dfList,dfCC)
                println("$file done ")
            catch e
                println("$file error", e)
            end
        end
    end
    # select!(dfList,Not(:Call))
    return dfList
end

#### MAIN CODE ########################

# """ SET Aux Folder """
cd("G:/My Drive/Booth/Political_firms/Data/AuxData")
# """Prepare dictionaries and variables"""
dfSV_hassan=CSV.read("EPU/FirmSVkey.csv",DataFrame)
dfComp=CSV.read("SAS/compustat_company.csv",DataFrame)
dfCompGvkeyUniqu=unique(dfComp,:gvkey)
dfCompT=dropmissing(dfComp,:tickersymbol) #drop companies without tickers
gvkey_dict_h = Dict(prepareName(row.company_name) => row.gvkey  for row in eachrow(dfSV_hassan))
gvkey_dict_c = Dict(prepareName(row.companyname) => row.gvkey  for row in eachrow(dfComp))
tickers=unique(dfCompT.tickersymbol)
ticker_gvkey_uniq=Dict()
for t in tickers #create dictionary with tickers, that are unique
    gvk=dfCompT[dfCompT.tickersymbol.==t,:].gvkey
    size(gvk)[1]==1 ? push!(ticker_gvkey_uniq,t=>gvk[1]) : nothing
end

firm_names_h=[k for k in keys(gvkey_dict_h)]
firm_names_c=[k for k in keys(gvkey_dict_c)]
firm_names=vcat(firm_names_h,firm_names_c)
# """ ************************************************************************ """


println("start linking CC to GVKEY")
cd("C:/CC/ConfCall20201024-20210405/CSV")
@time dfList=DoFolder()
CSV.write("CC_List.csv",dfList)
# """ END """
