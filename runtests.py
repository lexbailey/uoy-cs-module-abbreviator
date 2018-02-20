#!/usr/bin/env python
import gen

tests = []
with open("tests") as f:
    for line in f:
        tests.append(line.split(" - ", maxsplit=1))

passes = 0
fails = 0

for test in tests:
    if len(test) != 2:
        print("Bad test: %s" % test)
        continue
    target, fullname = test
    fullname = fullname.strip()
    result = gen.main(fullname).strip()
    if result == target:
        print("Pass: %s - %s" % (target, fullname))
        passes += 1
    else:
        print("Fail: %s should be %s - %s" % (result, target, fullname))
        fails += 1

print("%d passes, %d fails" % (passes, fails))
print("%.2f%% success rate" % (passes / (passes + fails) * 100))
