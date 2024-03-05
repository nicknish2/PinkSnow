using HTTP, Dates, Printf

path = "https://www.nohrsc.noaa.gov/nsa/discussions_text/Northeast/snowdepth/"
stations = ["HERMIT LAKE", 
            "MOUNT WASHINGTON",
            "HARVARD CABIN",
            "CARTER NOTCH",
            "ZEALAND FALLS HUT",
            "LONESOME LAKE HUT",
            "GROTON",
            "CRAWFORD NOTCH",
            "PINKHAM NOTCH",
            "JACKSON",
            "NORTH CONWAY",
            "MOUNT MANSFIELD",
            ]

year = DateTime(2024)
season_start = Day(-61)
season_end = Day(150)
frequency = Day(1)

timesteps_in_season = floor(Int,((year+season_end) - (year+season_start))/frequency)
season = [year + season_start + i*frequency for i in 0:timesteps_in_season]

for date in season
    
    yyyy = Dates.format(year,"yyyy")                # always use Jan year to name a season
    yyyymm = Dates.format(date,"yyyymm")
    yyyymmddHH = Dates.format(date,"yyyymmddHH")
    filename = "snowdepth_$(yyyymmddHH)_m.txt"
    fullpath = joinpath(path,yyyymm,filename)
    output_path = joinpath("data",yyyy,filename)

    try
        r = HTTP.request("GET", fullpath)
        success = true
    catch
        success = false
        @info "HTTP request failed: $date was not available."
    end

    if success
        txtfile = open(output_path,"w")
        body = split(String(r.body),"\n")

        # print header
        for line in body[1:2]
            println(txtfile,line)
        end

        # print stations
        for line in body[3:end]
            for station in stations
                if occursin(station,line)
                    println(txtfile,line)
                end
            end
        end

        close(txtfile)
        @info "$date written to file."
    end
end