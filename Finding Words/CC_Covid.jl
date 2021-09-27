#'''Covid Words Stat '''

using CSVFiles
using DataFrames
using CSV
using TextAnalysis
using Dates
using Plots
using ORCA
plotly()


function number_words(ng::Dict) #count number of words of whole documnt. ng - is a dictionary of documnt's documnt
    s=0
    for g in ng
        s+=g[2]
    end
    return s
end


function covid_Stat(cc,words)
    doc=StringDocument(cc)
    prepare!(doc, strip_punctuation | strip_html_tags | strip_non_letters)
    remove_case!(doc)
    ng=ngrams(doc,1)
    nw=number_words(ng)
    s=sum(map(w-> haskey(ng,w) ? ng[w] : 0,words))
    return s,s*1000/nw
end


function dfCovidStat(filename, dfCovid_master)
        dfCalls=CSV.read("$filename.csv")
        dfCovid=dfCalls[:,[:Title,:Date,:Report,:Call]]
        dfCovid[!,:Covid_n].=0
        dfCovid[!,:Covid_r].=0.0
        # words=["coronavirus","covid"]
        words=["coronavirus","covid","wuhan virus"]
        for row in eachrow(dfCovid)
            n,r=covid_Stat(row[:Call],words)
            row[:Covid_n]=n #count
            row[:Covid_r]=r # per 1000 words
        end
        select!(dfCovid, Not(:Call))
        append!(dfCovid_master,dfCovid)
end


function main_covid_stat()
    dfCovid_master = DataFrame(Title=String[],Date=Dates.Date[],Report=Int[],Covid_n=Int[],Covid_r=[])  #Covid_n - number CovWord per StringDocument
                                                                                                        #Code_r - number of CovWord per 1000 words
    files=readdir()
    for file in files
        if file[1:4]=="2020"
        # if file[end-2:end]=="csv"
            try
                filename=file[1:end-4]
                println(file)
                @time dfCovidStat(filename,dfCovid_master)
            catch e
                println(e)
            end
        end
    end
    CSV.write("CovidStat.csv",dfCovid_master)
    return dfCovid_master
end




cd("C:\\CC2019-20")


@time df=main_covid_stat()

dfCovStat=CSV.read("CovidStat.csv")

dfCovStat[!,:one].=1
dfCovStat[!,:is_cov].=dfCovStat[:,:Covid_n].>0


df=select!(dfCovStat,Not([:Title,:Report]))
dfCovid_agr=aggregate(df,:Date,sum)
sort!(dfCovid_agr,:Date)

```The number of "covid" words on CC Day```
plot(dfCovid_agr.Date,dfCovid_agr.Covid_n_sum,
    title="The number of \"COVID19\" words on CC Day",label="Covid",size=(1200,800))
    # scatter(dfCovid_agr.Date,dfCovid_agr.Covid_n_sum,
    #     title="The number of \"COVID19\" words on CC Day",label="Covid",size=(1200,800),smooth = true )
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\Number_of_Words_on_CCday.png")


```The number of "COVID19" words per Number of CC```
dfCovid_agr.Covid_perCC=dfCovid_agr.Covid_n_sum./dfCovid_agr.one_sum
plot(dfCovid_agr.Date,dfCovid_agr.Covid_perCC,
        title="The number of \"COVID19\" words per number of CC",label="Covid",size=(1200,800))
# scatter(dfCovid_agr.Date,dfCovid_agr.Covid_perCC, smooth = true,
#                 title="The number of \"COVID19\" words per number of CC",label="Covid",size=(1200,800))
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\Number_of_Words_per_numberCC.png")


```Percent of CC with even on "covid" word ```
```The number of CC with any \"covid\" words```
plot(dfCovid_agr.Date,dfCovid_agr.is_cov_sum,
    title="The number of CC with any \"COVID19\" words",label="Covid",size=(1200,800))
    # scatter(dfCovid_agr.Date,dfCovid_agr.is_cov_sum, smooth=true,
    #     title="The number of CC with any \"COVID19\" words",label="Covid",size=(1200,800))
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\Number_of_CC_with_anyCovid.png")

```Share of CC with even on "covid" word ```
dfCovid_agr[!,:Covid_share].=dfCovid_agr.is_cov_sum./dfCovid_agr.one_sum
plot(dfCovid_agr.Date,dfCovid_agr.Covid_share,
    title="Share of CC with even one \"COVID19\" word. ",label="Covid",size=(1200,800))
    # scatter(dfCovid_agr.Date,dfCovid_agr.Covid_share, smooth=true,
    #     title="Share of CC with even one \"COVID19\" word. ",label="Covid",size=(1200,800))
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\Share_CC_withCovid.png")

```Average number of "COVID19" per CC ```
dfCovid_agr[:,:Covid_n_av].=dfCovid_agr.Covid_n_sum./dfCovid_agr.is_cov_sum
plot(dfCovid_agr.Date,dfCovid_agr.Covid_n_av,
    title="Average number of \"COVID19\" words per CC with even one covid-word ",size=(1200,800),label="Covid")
    # scatter(dfCovid_agr.Date,dfCovid_agr.Covid_n_av,smooth = true,
    #     title="Average number of \"COVID19\" words per CC with even one covid-word ",size=(1200,800),label="Covid")
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\Numbe_ofCovidWord_per_CovidCC.png")
