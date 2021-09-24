``` 1) Parse all archive Thomson News file    (function ParseNews)
    2) Keep only unique News (AltId), by extract the oldest News item for the last update (function KeepUniqueAltId
    3) Parse Subjects fields into dummy columns for each category (ParseSubjects)
    4) The main function does 1)-2)-3) for each file in current category in parallel ```
using Dates
using DataFrames
using CSV
using Base.Threads
using CodecZlib
using BenchmarkTools


function ParseNews(line::String)
```Parse a News from text line. Return array of value, ready to insert into DataFrame ```

    keyword = "guid\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    Guid=line[fp+1:lp-1]

    keyword = "id\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    Id=line[fp+1:lp-1]

    keyword = "headline\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(", \"takeSequence",line,fp+1)[1]-1
    HeadLine=line[fp:lp]


    keyword = "body\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(", \"mimeType",line,fp+1)[1]-1
    Body=line[fp:lp]
    if length(Body)>4000000
        Body="Too big"
    end

    keyword = "versionCreated\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    VersionCreated=line[fp+1:lp-1]
    VersionCreatedDate  = Date(VersionCreated[1:findfirst("T",VersionCreated)[1]-1])
    VersionCreatedTime =  Time(VersionCreated[findfirst("T",VersionCreated)[1]+1:end-5])

    keyword = "firstCreated\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    FirstCreated=line[fp+1:lp-1]
    FirstCreatedDate  = Date(FirstCreated[1:findfirst("T",FirstCreated)[1]-1])
    FirstCreatedTime =  Time(FirstCreated[findfirst("T",FirstCreated)[1]+1:end-5])

    keyword = "mimeType\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    MimeType=line[fp+1:lp-1]

    keyword = "pubStatus\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    PubStatus=line[fp+1:lp-1]

    keyword = "language\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    Language=line[fp+1:lp-1]

    keyword = "altId\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    AltId=line[fp+1:lp-1]

    keyword = "takeSequence\": "
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    TakeSequence=parse(Int,line[fp+1:lp])

    keyword = "messageType\": "
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    MessageType=parse(Int,line[fp+1:lp])

    keyword = "subjects\": "
    fp=findfirst(keyword,line)[end]
    lp=findnext(", \"provider",line,fp+1)[1]-1
    Subjects=line[fp+1:lp]

    keyword = "provider\": \""
    fp=findfirst(keyword,line)[end]
    lp=findnext(",",line,fp+1)[1]-1
    Provider=line[fp+1:lp-1]

    keyword = "instancesOf\": "
    fp=findfirst(keyword,line)[end]
    lp=findnext(", \"id",line,fp+1)[1]-1
    InstancesOf=line[fp+1:lp]

    keyword = "urgency\": "
    fp=findfirst(keyword,line)[end]
    lp=findnext("}",line,fp+1)[1]-1
    Urgency=parse(Int,line[fp+1:lp])

    return [Guid, Id, HeadLine, Body,VersionCreatedDate,VersionCreatedTime,FirstCreatedDate,FirstCreatedTime,TakeSequence,MimeType,PubStatus ,Language ,AltId ,MessageType, Subjects ,Provider ,InstancesOf ,Urgency ]
end

```Parse a ZIP Text File of TRRN into DataFrame ```
function ParseNewsFile(file)

            #create DataFrame
            dfNews=DataFrame(Guid=String[], Id=String[], HeadLine=String[], Body=String[], VersionCreatedDate=Date[],VersionCreatedTime=Time[],
                            FirstCreatedDate=Date[],FirstCreatedTime=Time[], TakeSequence=Int[], MimeType=String[],PubStatus=String[],Language=String[],AltId=String[],
                            MessageType=Int[], Subjects=String[],Provider=String[],InstancesOf=String[],Urgency=Int[])

            #open ZIP File
            f=GzipDecompressorStream(open(file))
            readline(f) #the first line doesn't contain usefull information
            for line in eachline(f) #each line contain news item
                news_row =  ParseNews(line) #paser line of news
                push!(dfNews,news_row) #push into the DataFrame
            end
            close(f)
            return dfNews
end

``` Keep only unique AltId, by extract the oldset News item for the last update```
function KeepUniqueAltId(dfNews)

    dfNews.VersionCreatedDateTime=dfNews.VersionCreatedTime + dfNews.VersionCreatedDate
    dfNews_clean=similar(dfNews,0)
    deleterows!(dfNews,dfNews.MessageType.==7)
    deleterows!(dfNews,dfNews.MessageType.==8)

    for uid in unique(dfNews.AltId)
        id_set=dfNews[dfNews.AltId.==uid,:]
        push!(dfNews_clean,sort(id_set,[:VersionCreatedDateTime,:MessageType],rev=true)[1,:])
    end

    return dfNews_clean

end

function ParseSubjects(dfNews)

    for sn in SubjetNames
            SubjectOccurs = occursin.("N2:$sn\"",dfNews.Subjects)
            dfNews[:,Symbol(sn)]=SubjectOccurs
    end
    return dfNews
end

function main()
    files=readdir()
    Threads.@threads for file in files
           if file[end-1:end]=="gz"
            println("threadid-",threadid(), " ", file)
            dfNews=ParseNewsFile(file)
            println("threadid-",threadid(), " ","ParseNewsfile")
            dfNews=KeepUniqueAltId(dfNews)
            println("threadid-",threadid(), " ","KeepUnique")
            dfNews=ParseSubjects(dfNews)
            println("threadid-",threadid(), " ","ParseSubjests")
            filename=file[1:end-7]
            CSV.write("$filename.csv",dfNews)
        end
    end
end

```  -------------------  Main ---------------- ```
#redefine function: boolean type will write as 1 and Zero
CSV.writecell(buf,pos,len,io, x::Bool, opts) = CSV.writecell(buf,pos,len,io, x ? "1" : "0",opts)

#read all Categories

```Set Current Directory to the root of Political Firms folder ```
cd("G:\\My Drive\\Booth\\Political Firms")

dfSubjects=CSV.read("Data\\Temp\\Subjects.csv")
const SubjetNames=dfSubjects.SectionCode[1:end]

```set current folder to folder with raw files ```
cd("Data\\Raw\\RTRS_\\2019")


```Run Main fnction ```
@time main()
``` ---------------------------------------------- ```



#=
``` code to exstract all N2:* Categories
dfSubjects=dfSubjects[:,:]
for s in dfNews.Subjects[300001:end]
    println("new row")
    println(" ")
    for n2 in findall("N2:",s)
            sc=s[n2[end]+1:findnext("\"",s,n2[end])[1]-1]
            if size(dfSubjects[dfSubjects.SectionCode.==sc,:])[1]==0
                    push!(dfSubjects,["","","",sc,""])
                    println("push")
            end
    end
end


CSV.write("Subjects.csv",dfSubjects)
size(dfSubjects)
=#
