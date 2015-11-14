chmod u+x ./script/*.sh

pkill -9 socat
. ./pkill.sh

socat tcp-listen:10000,fork exec:./script/arm.sh &
socat tcp-listen:10012,fork exec:./script/arm16.sh &
socat tcp-listen:10014,fork exec:./script/bfin.sh &
socat tcp-listen:10015,fork exec:./script/cr16.sh &
socat tcp-listen:10005,fork exec:./script/cris.sh &
socat tcp-listen:10006,fork exec:./script/frv.sh &
socat tcp-listen:10001,fork exec:./script/h8300.sh &
socat tcp-listen:10016,fork exec:./script/m32c.sh &
socat tcp-listen:10007,fork exec:./script/m32r.sh &
socat tcp-listen:10008,fork exec:./script/mcore.sh &
socat tcp-listen:10002,fork exec:./script/mips.sh &
socat tcp-listen:10013,fork exec:./script/mips16.sh &
socat tcp-listen:10009,fork exec:./script/mn10300.sh &
socat tcp-listen:10003,fork exec:./script/powerpc.sh &
socat tcp-listen:10017,fork exec:./script/rx.sh &
socat tcp-listen:10004,fork exec:./script/sh.sh &
socat tcp-listen:10010,fork exec:./script/sh64.sh &
socat tcp-listen:10011,fork exec:./script/v850.sh &



