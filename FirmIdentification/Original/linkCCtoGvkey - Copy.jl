using CSV
using DataFrames
using StringDistances
#
# ```     parse CC datalist to match firm name to compustat gvkey and country ```
# ```     to match 3 source are using: 1) Hassan dataset 2) compustat capital IQ companies dataset 3) compustat capital IQ ticker ```
# ```     for unmatched firm's name, string distance comparison is using. ```


function getTicker(str) #``` parse tiker ```
    try
        # f=findfirst(" - ",str)[1]
        f=findfirst(" ",str)[1]
        p=f
        if !isnothing(findfirst(".",str[1:f-1]))
            p=findfirst(".",str[1:f-1])[1]
        end
        return replace(str[1:p-1],r"[\W]"=>"")
    catch
        return ""
    end
end
#



function deleteCorpWords(fname) #``` delete common words```
    words=["earnings conference call","conference call on productivity", "earnings release conference", "financial release conference",
        "conference call regarding", "earnings conference", "comprehensive review", "final transcript", "edited transcript",
        "week conference", "conference call", "edited brief", "preliminary brief", "earnings call", "earning call",
        "preliminary transcript", "final transcript", "call","cal","merger","c", "earning","earnings", "to discuss",
        "group","plc","ltd","limited","ag","corp","corporation","Incorporation","laboratories","labs","the","proposed","propose",
                        "holdings","oyj","inc","conference","co", "final","preliminary","and","&",
                        "company","trust","investment","investments","sln","sa","s.p.a.","spa","transc",
                        "quarter","st","nd","rd","th",
                        "q", "jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec",
                        ]

    fname = string(" ",fname," ")
    fname=replace(fname,r"[0-9]"=>" ")
    for w in words
        fname=replace(fname,Regex("\\b$w\\b") => " ")
    end

    return strip(fname)
end


function prepareName(fname) #""" prepare name for matching """
    fname=lowercase(fname)

    try
        f=findfirst("event transcript of",fname)[end]
        fname=fname[nextind(fname,f):end]
    catch
    end
    try
        f=findfirst("event brief of",fname)[end]
        fname=fname[nextind(fname,f):end]
    catch
    end

    try
        f=findfirst(" - ",fname)[end]
        fname=fname[1:f]
    catch
    end

    fname=replace(fname,r"\((.*)\)"=>"")
    fname=deleteCorpWords(fname)
    return strip(replace(fname,r"[.,'#-/0-9]"=>""))
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

function GuesNameTicker!(dfCC) #lookf through set of company names by tikers. (some tickers has several names) ```
    global cash_dict
    # dfCC[!,:prob].=1.
    # dfCC[!,:gues_by_dticker].=0
    # dfCC[!,:gues_name].=""
    for r in eachrow(dfCC)

            if r.gvkey==0
                firmname=prepareName(r.Title)
                #check cash
                if haskey(cash_dict,firmname)
                    cash=cash_dict[firmname]
                    r.prob=cash[1]
                    r.gues_name=cash[2]
                    r.gvkey = cash[3]
                    cash[4]==1 ? r.gues_by_dticker=1 : r.gues_by_dticker=0

                else
                    # println(r.ticker)
                    possible_compname= dfCompT[dfCompT.tickersymbol.==r.ticker,:] #set of possible company names
                    if size(possible_compname)[1]>1
                        prob=0
                        best_match=""
                        gvkey_match=0
                        for pn in eachrow(possible_compname)
                            p=compare(prepareName(pn.companyname),firmname,Jaro())
                            if p>prob
                                 prob=p
                                 best_match=pn.companyname
                                 gvkey_match=pn.gvkey
                            end
                        end
                        if prob>0.8
                            r.prob=prob
                            r.gues_name=best_match
                            r.gvkey=gvkey_match
                            r.gues_by_dticker=1
                            cash_dict[firmname]=[prob,best_match,gvkey_match,1]
                        end
                    end
                end
            end
    end
end


function GuesName!(dfCC)# """ mactch companies name by the best matched"""
    # dfCC[!,:prob].=1.
    # dfCC[!,:gues_name].=""
    global cash_dict
    for r in eachrow(dfCC)
        if r.gvkey==0
            fname=prepareName(r.Title)
            #check cash
            if haskey(cash_dict,fname)
                cash=cash_dict[fname]
                r.prob=cash[1]
                r.gues_name=cash[2]
                r.gvkey = cash[3]
                cash[4]==1 ? r.gues_by_dticker=1 : r.gues_by_dticker=0
            else
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
                cash_dict[fname]=[prob,best_match,gvkey_match,0]
            end
        end
    end
end

function MergeGvkey!(dfCC) #""" create the main gvkey based on three keys: hassan, compustat, tickers """
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
        dfCC=CSV.read("$filename.csv",copycols=true)

        #parse ticker from SubTitile
        dfCC[!,:ticker]=getTicker.(dfCC.Subtitle)
        #match three sources gvkeys
        dfCC[!,:gvkey_t].= getGVKey_ticker.(dfCC[:,:ticker])
        dfCC[!,:gvkey_h]=getGVkeyH.(dfCC.Title)
        dfCC[!,:gvkey_c]=getGVkeyC.(dfCC.Title)



        #Merge into one main gvkey
        MergeGvkey!(dfCC)
        #match firms without gvkey
        dfCC[!,:prob].=1.
        dfCC[!,:gues_by_dticker].=0
        dfCC[!,:gues_name].=""

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


function DoFolder(year)
    dfList=DataFrame()
    files=readdir()
    for file in files
        println(file)
        # if file[end-2:end]=="csv"
        if (file[1:4]==string(year))
            try
                dfCC=matchFile(file[1:end-4])
                append!(dfList,dfCC)
                # println("$file done ")
            catch e
                println("$file error", e)
            end
        end
    end
    # return dfList
    sort!(dfList,:prob)
    CSV.write("CC_List$year.csv",dfList)
end
#
println("start linking CC to GVKEY")

# """ SET Current Folder """
cd("C:\\Users\\jasonjia\\Dropbox\\Projects\\ConferenceCall\\Output\\ConferenceCall\\Csv")

#
# """Prepare dictionaries and variables"""
# types = Array{DataType,1}([String, Missing, String63, UInt32])
dfSV_hassan=CSV.read("C:\\Users\\jasonjia\\Dropbox\\Projects\\ConferenceCall\\Output\\FirmIdentification\\Hassan\\Hassanfile_raw_updated2019030_viewable.csv", DataFrame)
dfComp=CSV.read("C:\\Users\\jasonjia\\Dropbox\\Projects\\ConferenceCall\\Output\\FirmIdentification\\compustat_csv\\ciqcompany_mergedwithgvkeyandcountry_andnaivetickers.csv", DataFrame, copycols=true)
dfCompGvkeyUniqu=unique(dfComp,:gvkey)
dfCompT=dropmissing(dfComp,:ticker) #drop companies without tickers
# gvkey_dict_h = Dict(prepareName(row.company_name) => row.gvkey  for row in eachrow(dfSV_hassan))
nrows_dfSV_hassan = nrow(dfSV_hassan)
gvkey_dict_h = Dict()

for (rownumber, row) in enumerate(eachrow(dfSV_hassan))
    gvkey_dict_h[prepareName(row.company_name)] = row.gvkey
    if rownumber % 2500 == 0
        println(string(rownumber), " / ", string(nrows_dfSV_hassan))
    end
end

# gvkey_dict_c = Dict(prepareName(row.companyname) => row.gvkey  for row in eachrow(dfComp))
gvkey_dict_c = Dict()
nrows_dfComp = nrow(dfSV_hassan)
for (rownumber, row) in enumerate(eachrow(dfComp))
    gvkey_dict_h[prepareName(row.companyname)] = row.gvkey
    if rownumber % 2500 == 0
        println(string(rownumber), " / ", string(nrows_dfComp))
    end
end

tickers=unique(dfCompT.tickersymbol)
ticker_gvkey_uniq=Dict()
for t in tickers #create dictionary with tickers, that are unique
    gvk=dfCompT[dfCompT.tickersymbol.==t,:].gvkey
    size(gvk)[1]==1 ? push!(ticker_gvkey_uniq,t=>gvk[1]) : nothing
end

firm_names_h=[k for k in keys(gvkey_dict_h)]
firm_names_c=[k for k in keys(gvkey_dict_c)]
firm_names=vcat(firm_names_h,firm_names_c)

global cash_dict = Dict() # cash is already matched firms name
# """ ************************************************************************ """


#
# """ main code """
# cd("C:\\CC2010")
for i in 2001:1:2010
     @time DoFolder(2010)
end

# @time dfList=DoFolder()
# sort!(dfList,:prob)
# CSV.write("CC_List.csv",dfList)
# """ END """
