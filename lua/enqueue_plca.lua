
--[[

for DAM

]]
-- key1,argv1,argv2,argv3,argv4
-- KEYS[1], equipment
-- ARGV[1], timestamp
-- ARGV[2], cmd
-- ARGV[3], measurement
-- ARGV[4], data
-- ARGV[5], rawdata

-- eqpt_no,timestamp, cmd, measurement, data, rawdata

    local eqt = KEYS[1]
    local timestamp = ARGV[1]
    local cmd = ARGV[2]
    local measurement = ARGV[3]
    local vdata =cmsgpack.unpack(ARGV[4])
    local rawdata = cmsgpack.unpack(ARGV[5])

    local eqpt_key = string.format("%s_%s",KEYS[1],ARGV[2])

    local old_timestamp = redis.call("HGET", eqpt_key,"timestamp")

    if old_timestamp == false then
        redis.call("HSET",eqpt_key,"timestamp",timestamp)
        old_timestamp = redis.call("HGET",eqpt_key,"timestamp")
    end

    if timestamp - old_timestamp > 15 then

        old_timestamp =  redis.call("HSET",eqpt_key,"timestamp",timestamp)

        local s = {
                cmd = ARGV[2],
                rawdata = rawdata[0],
                data = {
                    measurement = measurement,
                    time = timestamp,
                    fields = {
                        FL_Open_Warning_View = vdata[0],
                        FR_Open_Warning_View = vdata[1],
                        RL_Open_Warning_View = vdata[2],
                        RR_Open_Warning_View = vdata[3],
                        FL_Close_Warning_View = vdata[4],
                        FR_Close_Warning_View = vdata[5],
                        RL_Close_Warning_View = vdata[6],
                        RR_Close_Warning_View = vdata[7],
                        LG_Open_Warning_View = vdata[8],
                        LG_Open_Warning_View = vdata[9],
                        DD_Close_Warning_View = vdata[10],
                        DD_Close_Warning_View = vdata[11],
                        H_Gas_Open_Warning_View = vdata[12],
                        DD_Close_Warning_View = vdata[13],
                        H_Pop_Open_Warning_View = vdata[14],
                        H_Pop_Close_Warning_View = vdata[15],
                        FL_Cycle = vdata[16],
                        FR_Cycle = vdata[17],
                        RL_Cycle = vdata[18],
                        RR_Cycle = vdata[19],
                        Pop_Hood_Cycle = vdata[20],
                        Gas_Hood_Cycle = vdata[21],
                        Decklid_Cycle = vdata[22],
                        Liftgate_Cycle = vdata[23],
                        FL_Ambient = vdata[24],
                        FL_Hot = vdata[25],
                        FL_Humid = vdata[26],
                        FL_Cold = vdata[27],
                        FR_Ambient = vdata[28],
                        FR_Hot = vdata[29],
                        FR_Humid = vdata[30],
                        FR_Cold = vdata[31],
                        RL_Ambient = vdata[32],
                        RL_Hot = vdata[33],
                        RL_Humid = vdata[34],
                        RL_Cold = vdata[35],
                        RR_Ambient = vdata[36],
                        RR_Hot = vdata[37],
                        RR_Humid = vdata[38],
                        RR_Cold = vdata[39],
                        Pop_Hood_Ambient = vdata[40],
                        Pop_Hood_Hot = vdata[41],
                        Pop_Hood_Cold = vdata[42],
                        Gas_Hood_Ambient = vdata[43],
                        Gas_Hood_Hot = vdata[44],
                        Gas_Hood_Cold = vdata[45],
                        Decklid_Ambient = vdata[46],
                        Decklid_Hot = vdata[47],
                        Decklid_Cold = vdata[48],
                        Liftgate_Ambient = vdata[49],
                        Liftgate_Hot = vdata[50],
                        Liftgate_Humid = vdata[51],
                        Liftgate_Cold = vdata[52],
                        EM_stop = vdata[53]
                              },
                    tags = {
                        eqpt_no =  eqt,
                        node = "1"
                            }
                }
            }

        local msg = cmsgpack.pack(s)  -- pack msg

        redis.call("RPUSH", "data_queue",msg) -- msg queue

        return s
    end