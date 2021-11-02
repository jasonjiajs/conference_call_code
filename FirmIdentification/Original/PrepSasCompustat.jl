#```read compustat.sas files to get  gvkey and firm's country informtion.  ```
#``` join to hassan firm list data set ```


using CSV
using DataFrames
using SASLib


#read company list
dfComp_sas=DataFrame(readsas("G:\\My Drive\\Booth\\Political_Firms\\Data\\sas\\ciqcompany_query.sas7bdat"))
dfCountry_sas=DataFrame(readsas("G:\\My Drive\\Booth\\Political_Firms\\Data\\sas\\ciqcountry.sas7bdat"))
dfComp_sas=join(dfComp_sas,dfCountry_sas, on = :countryid)
#CSV.write("G:\\My Drive\\Booth\\Political_Firms\\Data\\sas\\compustat_company_full.csv",dfComp_sas)

dfGvkey_sas=DataFrame(readsas("G:\\My Drive\\Booth\\Political_Firms\\Data\\sas\\wrds_gvkey.sas7bdat"))
CSV.write("G:\\My Drive\\Booth\\Political_Firms\\Data\\sas\\compustat_company_GVkey.csv",dfGvkey_sas)
dfComp_sas=join(dfComp_sas,dfGvkey_sas[:,[:companyid,:gvkey]], on = :companyid)
dfComp_sas[!,:gvkey].=parse.(Int,dfComp_sas[:,:gvkey])
dfComp_sas=sort(dfComp_sas,:gvkey)

dfComp_sas=join(dfComp_sas,dfCountry_sas, on = :countryid)
CSV.write("G:\\My Drive\\Booth\\Political_Firms\\Data\\sas\\compustat_company.csv",dfComp_sas)
