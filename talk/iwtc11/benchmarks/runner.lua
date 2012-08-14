require('scimark')
require('stats')
local pi, clock = math.pi, os.clock

local benchmarks = {}

function benchmarks.SOR(n, cycles)
    n, cycles = tonumber(n), tonumber(cycles)
    local mat = scimark.random_matrix(n, n)
    scimark.sor_run(mat, n, n, cycles, 1.25)
    return string.format('SOR(%d, %d)', n, cycles)
end

function measure(name, ...)
    scimark.array_init()
    scimark.rand_init(101009)
    local run = benchmarks[name]
    io.stderr:write('waming up')
    for i=1,3 do
        run(...)
        io.stderr:write('.')
    end
    io.stderr:write('\n')
    io.stderr:write('benchmarking\n')
    all = {}
    for i=1,10 do
        local tm = clock()
        fullname = run(...)
        tm = clock() - tm
        io.stderr:write(string.format('Next: %f\n', tm))
        table.insert(all, tm)
    end
    io.write(string.format('%s: %f +- %f\n', fullname, stats.stats.mean(all), stats.stats.standardDeviation(all)))
end

local function main(args)
    measure(unpack(args))
end

main(arg)

