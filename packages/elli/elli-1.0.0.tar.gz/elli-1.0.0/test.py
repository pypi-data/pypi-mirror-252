from pathlib import Path
from intelhex import IntelHex
from elli import Elli

zephyr = Path("/home/austreng/SecDom/build/zephyr/zephyr.hex")

ih = IntelHex(str(zephyr))
el = Elli(zephyr)

assert {k: v for k, v in ih.todict().items() if isinstance(k, int)} == el.to_dict()
assert ih.todict()["start_addr"]["EIP"] == el._exec_start_address


reconst_hex = el.to_hex()

outfile = Path("./out.hex")
outfile.write_text(reconst_hex)

ih2 = IntelHex(str(outfile))
el2 = Elli(outfile)

assert {k: v for k, v in ih2.todict().items() if isinstance(k, int)} == el2.to_dict()
assert ih2.todict()["start_addr"]["EIP"] == el2._exec_start_address

assert {k: v for k, v in ih.todict().items() if isinstance(k, int)} == el2.to_dict()
assert ih.todict()["start_addr"]["EIP"] == el2._exec_start_address

assert el2.to_dict() == el.to_dict()
assert el2._exec_start_address == el._exec_start_address

assert el2._start_segment_cs == el._start_segment_cs
assert el2._start_segment_ip == el._start_segment_ip
