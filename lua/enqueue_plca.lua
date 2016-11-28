
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
                        FL_Open_Warning_View = vdata[1],
                        FR_Open_Warning_View = vdata[2],
                        RL_Open_Warning_View = vdata[3],
                        RR_Open_Warning_View = vdata[4],
                        FL_Close_Warning_View = vdata[5],
                        FR_Close_Warning_View = vdata[6],
                        RL_Close_Warning_View = vdata[7],
                        RR_Close_Warning_View = vdata[8],
                        LG_Open_Warning_View = vdata[9],
                        LG_Open_Warning_View = vdata[10],
                        DD_Close_Warning_View = vdata[11],
                        DD_Close_Warning_View = vdata[12],
                        H_Gas_Open_Warning_View = vdata[13],
                        DD_Close_Warning_View = vdata[14],
                        H_Pop_Open_Warning_View = vdata[15],
                        H_Pop_Close_Warning_View = vdata[16],
                        FL_Cycle = vdata[17],
                        FR_Cycle = vdata[18],
                        RL_Cycle = vdata[19],
                        RR_Cycle = vdata[20],
                        Pop_Hood_Cycle = vdata[21],
                        Gas_Hood_Cycle = vdata[22],
                        Decklid_Cycle = vdata[23],
                        Liftgate_Cycle = vdata[24],
                        FL_Ambient = vdata[25],
                        FL_Hot = vdata[26],
                        FL_Humid = vdata[27],
                        FL_Cold = vdata[28],
                        FR_Ambient = vdata[29],
                        FR_Hot = vdata[30],
                        FR_Humid = vdata[31],
                        FR_Cold = vdata[32],
                        RL_Ambient = vdata[33],
                        RL_Hot = vdata[34],
                        RL_Humid = vdata[35],
                        RL_Cold = vdata[36],
                        RR_Ambient = vdata[37],
                        RR_Hot = vdata[38],
                        RR_Humid = vdata[39],
                        RR_Cold = vdata[40],
                        Pop_Hood_Ambient = vdata[41],
                        Pop_Hood_Hot = vdata[42],
                        Pop_Hood_Cold = vdata[43],
                        Gas_Hood_Ambient = vdata[44],
                        Gas_Hood_Hot = vdata[45],
                        Gas_Hood_Cold = vdata[46],
                        Decklid_Ambient = vdata[47],
                        Decklid_Hot = vdata[48],
                        Decklid_Cold = vdata[49],
                        Liftgate_Ambient = vdata[50],
                        Liftgate_Hot = vdata[51],
                        Liftgate_Humid = vdata[52],
                        Liftgate_Cold = vdata[53],
                        EM_stop = vdata[54]
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