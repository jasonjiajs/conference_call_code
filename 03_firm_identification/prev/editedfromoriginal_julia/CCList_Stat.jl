#various statistics over Conference Calls list
using CSV
using DataFrames
using Dates
using Plots
using ORCA
plotly()


function readFolder() #read folder with CC_list per year file and merge into one file
    dfCClist=DataFrame()
    files=readdir()
    for file in files
        if file[8:9]=="20"
            println(file)
            df=CSV.read(file)
            append!(dfCClist,df)
        end
    end
    return dfCClist
end

cd("C:\\temp\\final") #folder with CC_list per year files.

#read all CClist
dfCC=readFolder()

#keep unique reports, due to being possible dublicate
unique!(dfCC,:Report)

#keep only wth high probability
good_matched_share = sum((dfCC.prob.>0.9) .| (dfCC.gues_by_dticker.==1))/size(dfCC)[1]
dfCC=dfCC[(dfCC.prob.>0.9) .| (dfCC.gues_by_dticker.==1),:]

dfCC[!,:year].=Dates.year.(dfCC.Date)
dfCC[!,:month].=Dates.month.(dfCC.Date)
dfCC[!,:quarter].=Dates.quarterofyear.(dfCC.Date)

CSV.write("CC_ListTotal.csv",dfCC)
dfCC=CSV.read("CC_ListTotal.csv")


#number of unique Firms
dfFirms=number_unique_firms=unique(dfCC,:gvkey)
CSV.write("CCFirms.csv",dfFirms)
  # dfFirms = CSV.read("CCFirms.csv")

########f FIGUERES ###########################################################
function agregateByYear(df)
    df[!,:one].=1
    return rename!(aggregate(df,:year,sum),:one_sum=>:qty)
end

######## number of firms by year
dfFirm_year=agregateByYear(dfFirms[:,[:year]])
plot(dfFirm_year.year,dfFirm_year.qty,label="Total")
dfFirm_year=agregateByYear(dfFirms[dfFirms.countryid.==213,[:year]])
plot!(dfFirm_year.year,dfFirm_year.qty,label="US")
Plots.savefig("G:\\My Drive\\Booth\\Political_Firms\\Documentation\\tex\\Figures\\CCFirm.png")

######## number of reports by year
dfCC_year=agregateByYear(dfCC[:,[:year]])
plot(dfCC_year.year,dfCC_year.qty,label="Total")
dfCC_year=agregateByYear(dfCC[dfCC.countryid.==213,[:year]])
plot!(dfCC_year.year,dfCC_year.qty,label="US")
Plots.savefig("G:\\My Drive\\Booth\\Political_Firms\\Documentation\\tex\\Figures\\CCRepots.png")


function agregateByCountry(df)
    df[!,:one].=1
    return rename!(aggregate(df,:country,sum),:one_sum=>:qty)
end

dfCC_country = agregateByCountry(dfCC[:,[:country]])
sort!(dfCC_country,:qty,rev = true)
dfCC_country[!,:shr].=dfCC_country.qty./size(dfCC)[1]

dfFirms_country = agregateByCountry(dfFirms[:,[:country]])
sort!(dfFirms_country,:qty,rev = true)
dfFirms_country[!,:shr].=dfFirms_country.qty./size(dfFirms)[1]
dfFirms_country[1:10,:]

function LatexTab(df,header,file_name)
    columns = names(df)
    # header=string(columns[1], join(string(" & " , cl) for cl in columns[2:end] ), "\\\\ \\hline \n")

    row_tex(r) =  string(r[1], join(string(" & " , round(cl;digits=3)) for cl in r[2:end] ), "\\\\  \n")
    tex=string(header,"\n",join(row_tex(r) for r in eachrow(df)))

    open(file_name, "w") do io
           write(io,tex)
       end;
end

LatexTab(dfCC_country[1:20,:],"Country & Quantity & Share (\\%) \\\\ \\hline",
"G:\\My Drive\\Booth\\Political_firms\\Documentation\\tex\\top20CC_countries.tex")


LatexTab(dfFirms_country[1:20,:],"Country & Quantity & Share (\\%) \\\\ \\hline",
"G:\\My Drive\\Booth\\Political_firms\\Documentation\\tex\\top20frm_countries.tex")

################## histogram firm's life time ##########################

function checkYearGvkey(year,gvkey)
    return sum(dfCC[dfCC.year.==year,:].gvkey.==gvkey)>0
end

@time for y in 2001:2020 #create columns y$year = unmber of firm reports per year
    # println(y)
    dfFirms[!,Symbol("y$y")].= [checkYearGvkey(y,r.gvkey) for r in eachrow(dfFirms)]
end

dfFirms[!,:year_t].=0

for r in eachrow(dfFirms) #count how many year firm was reporting.
    r.year_t= sum(r[27:46])
end

histogram(dfFirms[:,:year_t],label="")
Plots.savefig("G:\\My Drive\\Booth\\Political_Firms\\Documentation\\tex\\Figures\\life_year_hist.png")


########### Compare Hassan firms and CC Frims. ########################################

#load hassan's firms dataset (names are unique, gbkey aren't unique)
dfHassan=CSV.read("G:\\My Drive\\Booth\\Political_Firms\\Data\\EPU\\FirmSVkey.csv")
dfHassan= unique(dfHassan,:gvkey)#keep unique

#select Hassan's firms doesn't mathed
dfHassan_anti=join(dfHassan,dfFirms,on = :gvkey,kind=:anti) #dfFirms - dataset of unique CC Firms

#select firms mathed by hassan.
dfCC_gh=unique(dfCC[:,[:Title,:gvkey_h]],:gvkey_h)
dfCC_gt=unique(dfCC[:,[:Title,:gvkey_t]],:gvkey_t)

#Unmatched Hassan Firms
dfNotMatched = join(dfHassan_anti,dfCC_gh,on = :gvkey => :gvkey_h,kind=:anti)
dfNotMatchedHassan = join(dfNotMatched,dfCC_gt,on = :gvkey => :gvkey_t,kind=:anti)
CSV.write("G:\\My Drive\\Booth\\Political_Firms\\Data\\Result\\UnmatchedHassan.csv",dfNotMatchedHassan)

#share of Hassan's dataset which are unmatch by our code.
Hassan_unmatch_share = size(dfNotMatchedHassan)[1]/size(dfHassan)[1]


########## Unmatched by year ##############################################

function MatchStatbyYear(dfCC,year)
    dfCC_y=dfCC[dfCC.year.==year,:]
    s=size(dfCC_y)[1]

    return [Int(year),
            sum(dfCC_y.gvkey_h.!=0)/s,
            sum(dfCC_y.gvkey_t.!=0)/s,
            sum(dfCC_y.gvkey_c.!=0)/s,
            sum(dfCC_y.prob.<1)/s,
            sum((dfCC_y.gvkey_h.!=0) .& (dfCC_y.gvkey_t.==0) .& (dfCC_y.gvkey_c.==0))/s,
            sum((dfCC_y.gvkey_h.==0) .& (dfCC_y.gvkey_t.==0) .& (dfCC_y.gvkey_c.!=0))/s,
            sum((dfCC_y.gvkey_h.==0) .& (dfCC_y.gvkey_t.!=0) .& (dfCC_y.gvkey_c.==0))/s]
end



dfMatchStat=DataFrame(year=Int[],H=Float32[],T=Float32[],C=Float32[],U=Float32[],Ho=Float32[],Co=Float32[],To=Float32[])
for year in 2001:2020
     push!(dfMatchStat,MatchStatbyYear(dfCC,year))
end


plot(dfMatchStat.year,dfMatchStat.U,label="String distance")
plot!(dfMatchStat.year,dfMatchStat.H,label="Hassan")
plot!(dfMatchStat.year,dfMatchStat.T,label="Ticker")
plot!(dfMatchStat.year,dfMatchStat.C,label="Compuastat")
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\MatchSources.png")


plot(dfMatchStat.year,dfMatchStat.Ho,label="Hussan only")
plot!(dfMatchStat.year,dfMatchStat.To,label="Ticker only")
plot!(dfMatchStat.year,dfMatchStat.Co,label="Compustat only")
Plots.savefig("G:\\My Drive\\Booth\\Political Firms Doc\\Update Working Folder\\Figures\\UniqueSources.png")


###############################################################################################################
dfCC_gues=select(dfCC[dfCC.prob.<1,:],[:Title,:gvkey,:prob,:gues_name])
dfCC_gues=dfCC_gues[dfCC_gues.gvkey.!=-1,:]
unique!(dfCC_gues,:gvkey)
sort!(dfCC_gues,:prob)

CSV.write("G:\\My Drive\\Booth\\Political_Firms\\Data\\Result\\CC_guess.csv",dfCC_gues)
