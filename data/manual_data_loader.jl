using HTTP, Dates, Printf

path = "https://www.nohrsc.noaa.gov/nsa/discussions_text/Northeast/snowdepth/"

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
        txtfile = open(output_path,"w")
        println(txtfile,String(r.body))
        close(txtfile)
        @info "$date written to file."
    catch
        @info "HTTP request failed: $date was not available."
    end
end