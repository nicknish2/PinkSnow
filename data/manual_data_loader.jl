import Pkg; Pkg.add("HTTP")

using HTTP, TOML, Dates, Printf
stations = TOML.parse(open("data/stations.toml"))["stations"]

path = "https://www.nohrsc.noaa.gov/nsa/discussions_text/Northeast/snowdepth/"

year = DateTime(2024,1,1,12)
season_start = Day(-61)
season_end = Day(150)
frequency = Hour(24)

timesteps_in_season = floor(Int,((year+season_end) - (year+season_start))/frequency)
season = [year + season_start + i*frequency for i in 0:timesteps_in_season]

for date in season
    
    yyyy = Dates.format(year,"yyyy")                # always use Jan year to name a season
    yyyymm = Dates.format(date,"yyyymm")
    yyyymmddHH = Dates.format(date,"yyyymmddHH")
    filename = "snowdepth_$(yyyymmddHH)_m.txt"
    fullpath = joinpath(path,yyyymm,filename)
    output_path = joinpath("data",yyyy,filename)

    success::Bool = false
    body::Vector{SubString{String}} = []
    try
        r = HTTP.request("GET", fullpath)
        body = split(String(r.body),"\n")
        success = true
    catch
        @info "HTTP request failed: $date was not available."
    end

    if success
        try
            mkdir(joinpath("data",yyyy))
        catch
            nothing
        end
        txtfile = open(output_path,"w")

        # print header
        for line in body[1:2]
            println(txtfile,line)
        end

        # print stations
        for line in body[3:end]
            id = split(line,"|")[1]
            if id in stations
                println(txtfile,line)
            end
        end

        close(txtfile)
        @info "$date written to file."
    end
end
