'''
Technical Indicator Node Unit Tests

To run unittests:

# Using standard library unittest

python -m unittest -v
python -m unittest tests/unit/test_nodes.py -v

or

python -m unittest discover <test_directory>
python -m unittest discover -s <directory> -p 'test_*.py'

# Using pytest
# "conda install pytest" or "pip install pytest"
pytest -v tests
pytest -v tests/unit/test_nodes.py

'''
import warnings
import unittest
import cudf
from greenflow_gquant_plugin.transform import ReturnFeatureNode
from greenflow_gquant_plugin.transform import IndicatorNode
from greenflow_gquant_plugin.transform import AssetIndicatorNode
from greenflow.dataframe_flow.task import Task
from .utils import make_orderer, error_function_index
import numpy as np
import pandas as pd

ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare

# gt for  return
ground_truth = b'\x92\x01\xef3\xec \x02@\xa3\xd5\xc0\xd96\xdd\xc0\xbf\xe2\xe1\xa7f\xab\xc0\xaa?\x8e\x9cySv\x9b\xca?vA\xc5\xd9\x8e\xd6\xd8\xbf\xbf){\x92=p\xc3\xbf\xd7\x06\xda\xca\x98\n\xd0?\xcf\xbf\xe8C\xb8\xb5\xc6?\x03\xa9\xf2H1\xcf\xca?V{\xc3\x9c\xda\xd5\xc0?\x1f\xed\xc6p\x14\xea\xe4\xbf\x84*\x911\x07\xf6\xe1\xbfQ\xdbQON&\x12@b\\H\xceZ\x19\xd3\xbfsxy\xfe\x9aT\xdf?\xc08\x16\xc2\xe0\xef\xdc\xbflI\xa2\xf0\xbfo\xee?\xc7\x0f\xffY\xa0\x00\xd7\xbf\x04l\xf3\xfcD\x16\xe1\xbf\xb9j]\x90my\xe8\xbf[\xc0B\x82\xe6\xf5\xe1?h$\xf1\x99\xec\x9f\xec?\xf1#\xdb\xb9GX\xf8?\xcd\xaf\xe4\x1b\xc0\x13\xeb?\xa8`\xa6\x8d\x8af\xbf?m\'\x07\x92j\x80\xd7\xbf<\xa4\x04\xfb\x93\xa7\xdf\xbf\xd3\xdd\xbcGk\xd1\xf3?\xf9"\xc8w\xad\xc8\x95\xbf:3\xe3\x05\xef\xf4\xca\xbf\nU\xd1\tQ[\xed?\xd3\x8f\xc0\x87J\x0f\xc5\xbf\r6\n[\xb1T\xc3?\xd5I\x83\xa6\xee\xae\xd5\xbf]\xc3\x1f\xc6L/\xe3?I\xe3K\x1b\xf6f\xd1\xbf\xaf+ =\xc9\x9c\xef\xbf{\xd6\x94\xb3R#@@\t\xe8\xe6D\x83\xb8\xfe?\xc2\x01\'3NJ\xde\xbf\xea\x98j\xdc9\x81\xe3\xbf\xb2.\xf1\x9e\xcd\xa4\xd5\xbf\xf2Q\xbf\x0c\xf1\xdd\x17@\xf4\x05\xf44>\xe6\xc7\xbf$\xfc\xee?&\x07\xcd\xbf\r\x1d\x0eg\xb6\x90\xdb\xbfu\xbe\x9d\xde\t\xaa\xf3?\x18\xa0\xb6\x11\x83\xf9\xda\xbf\x97X=\xaa\xe5\xbe\xdd?\xca\xf6\xcb_re\xda?\xdc\xc3\x92tf$\xba?\xc5\xd6{8G\x00\xec\xbf\xddo\xd4\x8c\xc8\xeb\x0e@\x06\xd7\xfe\x9c\x00\xe7\xd0?\xca\x90F\x90gi\xe8\xbf F\x85<\xd3\xa1\xef\xbf\xd6A\x15\x00\x8a$\x81@/\xfbQ$\xbb\x11\xc5\xbf\xaf\xfeh\x1f\xe0$\xe5\xbf?o\x97\x9b\x87\xc3\x92?\xc4{\xe6\xbd\xbd)\xe2\xbf\\\x16\x0fp\x8b\xdd\x07@y\xa0,;\x81\x10\xee?-\x94\xe8C]\x15\x93\xbf\xd4b\xc0gix\xe7\xbf\x9bm\x8c\xe8\xab\xcf\xe3?m\xa9\x12H\xa0P\xf7?\xbf\xc3\x11\x0e\xde\xe8\xe6\xbfT*=\xf3\xb78\x03@\x8aY"\x8c\x17\x0b\xc7\xbfOy\xe8sPB\xc3?\x98j\xe1\xbd\xcd\xbe\x8f\xbf\xb0W\xa1Dh\x9e\xea\xbf\xc0\xa3\xb1\xb4U\x8d\x11@4\xfc\xaaY\xecw\xc3?\x90\xde):Y\x01\xb4\xbf\xc5\x15\xfdg`C\xc3\xbf\xae\xa3\x88\x92\x90/\xe2\xbf\xce{^\xef\xfdR\xc3?\xb4\xbeN\xd5P>\xd5\xbf\x97\xd9e\xc3!\xd7\xe3\xbf\xd7+#\x11{\xa5\xf2?1\x1b\xc6^\xeaT\x01@\xe8\x1eV\xa0^o\xe0?\xfb\xc7\x92\x02@\x8c\xd0\xbfm\xfa\x9fef\xc0\xc7\xbf\xc7\xf0\xf4r%\x01\xe1\xbf\r\rv&\xac\xf4\xef?vh\xd4\xfcQ\xd4\xe0?\xde\xa3\xab\x04\xe3B\xe4\xbf\xfd\x03)\xaa.<\xd8\xbf\x89.\x8c\x9aN\x8e\xec\xbf\x0b2M\xb3\xc1UB@\x16\x80^\xcc\xf9Y\xee\xbf[\xb63\xe7}\xa6$@|\x0eb$\xaee\xed?%Y(\x9b\x7f{\xef\xbf\xb10[\xd1\x1flB@\x06\xaf\'\x19I\xf1\xad\xbf\xea_\xa2\x15\xf0\xaa\xe3\xbf=\xd9q\xa9U\t<@>\xef\x06{~\x13\xea\xbf\xce!\xaf\xce\x80y!@\x17*T\x8ae\xc9\xde?\xcc\xe4\xa01\x0c\x1d\xe1\xbf\x18\x9c\xc1\rC\x07\xed\xbf"k\x95 \xfc\xcb\xf1?\xc9e\xf6b&)\x8b?\xe6^\xd1\x03\xe2\xc2!@P",%^\xf2\x85\xbfV\x06\x94]\xfeR\xef\xbf\x9d\xfa\x88\xad\xa0\xf7H@\xf5\x84\x17;\xe9\xb9\xad?$|\xa9\xb1`\xec\xe1\xbfW\x8fd\xd3\xa72\xd2\xbf\xe9\xf3\xd8!U\x04\xff?\x8d\xec7d)(\xd1\xbf\xde\x06C\x7fb\xb5\xe8\xbf\xccF$ux\x10\xe4?E\xc2\xcbD\xc0m\x05@\xceS\x8c1\xd8\xd8k?\x18\xce\xa7z"\xa8\xe7\xbf<s8M\xf2y\x05@\x0e\x1aK\xe8b\xb6\xd5\xbf_O\xb0_^\xc9\xc1?{\x92*\x07~&\xc2\xbf\xcf\xac\xcc\x80\xbaH\xcc?\xe3G\xe6\xe1\xf5\xbd\xef\xbf\x7f\x82\x84\x12\xc2a\x0e@\xa7G^\x88z\xe4:@\x9c\xd1\xf3\x92\xd8\n\xe8\xbf\x8b@\xa2\xa66Z\x08@2&@\xd9`\xd8\xe2\xbfj\x08\x1f\x9e\x84\xd1\xe9\xbf\x8f5\xc9L\x8c!#@UX\xa0\x07\x89{\xdf\xbf\\]\x89\xfe\x08]\xb7?\xe7\x92B\xcb|\xed\xff?\xe2b\xe0\xb3\x94\x8c\xe9\xbf\x80H\xbf\x93\x1b\x07\xe9?2\xf6u@;k\xe6\xbf\x97.e%\xf1\xe6\x06@\x8f\xf9\x91\xc9\xe9\x9a\xe8\xbfU7\xa1\xe7\xd4\xbf\x11@L\xadA\x91\xbe#\xde?\xcf\xba\xfc\x0f\xa3\xc5\xef\xbf\x7f+\'_\xc4\n0@1=;4M\x1e\xd8\xbf\x060E~\xc9z-@3y\x08I<P\xbd?\x8d\x02\xbd\xf2\xd08\xde\xbf\x8dU\xc4I6\xcb\xe3\xbf\x0bc"\x89\xb7\xa1\r@\xc8\x17\xf79.\x1d\xd3\xbf\x8cyq\x04\xa9\xd3\xca?`\xb2\xb5R\xc4\xad\xd6\xbf\xfcF\xc90\xbdV\xe1?\x14\x94D\xc3hh\xe2\xbf\x8e|\x0cY\xdb,\xe5\xbf?\xe7\xcf\xb3\x0c\xf5\x1b@\xb9|\x12\xef\xc1\xd9\xef\xbf\xdd\xf1U2\xdff0@\x88\xff\x1e\xe9\xdb\x97\xe9?\xab\xdc\x95\xc1\xb3|\x18@\xba_\xc38\x06\xb6\xe5\xbfK\x05\xd9\x0c\xee\xee\xd2\xbf\xaf\x0c\x85|\x80i\xc9?\xcc\xd0\x90\xab\x81\xfe\xe3\xbf\xadEW\xcb\xd4\x82\t@\x10\xd2\xeett8\xea?\x91\xc9R?\x89\x00\xbd\xbf\xf7R\xb0\xe9\xd7\x9d\xe3\xbf%\x1eK\xcc;\xe3\xb7\xbf\x1ce\x80\x92D\xe1\xf2?XO\xaf\x94\xdd\xcf\xe7?iB \x9e\xe8\x12\xd1\xbf\xd5B\xf0t\xadO\xc8?>\x89x\xa3\xc1\xeb\xda\xbf\r\x1c\xf50\xec\x9d\xb5\xbf\x95FF\xe8z\xcd\xe9?}^\xbd\x94\xba\x08\xdf\xbf\xdd\xf3I\x96\xfd\xf9\xde?\xdcl-c*W\xeb\xbf\x86\xd4\xfe\x0b\xe6\x8a\x19@n\x9f\xf5\x1c\x8a\xdf\xe0\xbf`\xa2JiRI\xfa?\x88\xfb\x95\xcb\xce\x1e\xe3\xbf\x01q\xf5V~\x8f\xf8?;\xd6\x8dX$p\xe6\xbf\xec*\xb9\x9f|`\xef\xbfI\xbd\xbd\xa5\x90\xb6>@\xc4\x92\\\x81\xcd\xda\xf1?\x9c\xcdf\xe3\xf7\xac\xd5\xbfH\xc6\x8d\xbbU\xe6\xfc?=i\xb19\xe4\xc1\xe3\xbf\xa5b\xc3oo\xa8\x05@\x97\x17\x10\x8e\x84\'\xd8\xbf\x8f=z\xe6\x1al\xd4?'  # noqa #E501

# gt for indicators
g_t1 = b'\x80x\xe2\xf8Q\x0f\x7f\xbf\x04O\x11|\xec\x0e\xdd?\xa0\xbf\x98\x96\x03\x97\xca?\xf7\xbbF\xea;I\xd0?\x02\x8e\x80\xa6n\xf5\xcd?\xf85`\x18)\xd1\xc3?/\x12n\xb1\xb1\xaa\xc8?\x88^c<\xeb\xe5\xa3?d\xce[\x8f\xd73\xb0?$\xfe\xba\x87\xecq\xb2?(\x87\x87\xfcTF\xbf?\x1ezq\xeee\x13\xd2?\xccPQ\x90\xb4\xf5\xcd\xbf\xa8\xd0\xfd\xf9\x1c\xfd\xc1\xbf\x92\xfdI\xf3\xb6\xdf\x05\xc0m\xd5\xff\xd84\xb4\x00\xc0\x8c)\x9c\x0c\x86\x08\xf6\xbf\xb0\xeb\xb4x\x83\xad\xea\xbf\xf4\xdc{HY\xe3\xe1\xbf\xc0j\xb9I\x8c/\xce\xbf y\xe5\xe1\x15\xa0\xb4?L\x0b\xactJ\xe6\xd2?\x14i\\\x0c\xae\x1e\xdc?\xb8\xe2\xc0\x98\x19\x19\xd8?\x8c\xfa\x1fRG[\x06@:\xa4S\x87\xfek\x02@\xf5w\x95\xf5\xc6{\xfc?\x9a\xa5\x94Z\xee\xdc\xf5?\xfa7;\x04\xc7\xc9\xf1?\x95QY\xa3\xa3\xa3\xd2?\xc7\xfe\xe6J\xfb\x84\xa0?f\x1d\x97G\xd3s\xd7\xbf\x14\x11;z\xfbX\xc1\xbf<\xd0<\xdb\xf2\x01\xb8\xbf>bq\x8aG\x18\xc7\xbf\x98\xb0\x83\xf6\x16L\xc0\xbf`\xb9\xd6NE\x9d\x9e?GT\xdb\x9cT{\xd0?\x1a\xc1\xa9\x86\xa7\xe1\xc7?Z\xa0\xf8\x7ff\x0b\xb3?(\x8bT\\\xb2\xcc\x7f?=\xceH\xdckF\xd4?D\x1fV\x8cHG\xd6?2B\xcd5\xa3\xb1\xd0?\x8aI\xe5Kt.\xc4?Ta<\xe3$\'\xbf?p\xc5\x8b\xb5Yu\x8e?\xf0\xe0(\x8a)=\xa0\xbf4\xe1\xf02u\x85\xc3\xbf\x18\xb6\xbbYrm\xc5\xbf\xc6\xc2\xe0BV\x1d\xc5\xbf8\x8cO\xb3\xbfH\xb4\xbf\x1c\xfe|Yt,\xc4?\xd3\x99\xc8b=\x02\xc0?\xac\x99\xe6\x00\xb9\xb9\xc1?\x04U\xd9\x98\xc3\xa5\xbf?\xbeRe\x1d\xba\xe5\xc4?\xa80o\xfc#\x12\xbb?p1\\\xc4\xb5\x86\x9a?\xe4\x19\xe2Ch\x9d)@_\xc7\xe8;\xea6"@\xba\xac\xae\xa0\x8aA\x1e@Xgp\xb4\x90\xdfM\xc0$\xacd\x8d\x11\xd1E\xc0`\xf4\xf3+p`?\xc0\xba!\x19\x10\x8aZ5\xc0X\xc9\x8e\xdc\xd1Y+\xc0\xd8\xc8\xab\xd8] \x1f\xc0\xb0\x03\xac\xd4\x1a\xa1\t\xc0\x80\xf2g\x98\xa5h\xcd?\xe0\x8b\xf8\xda\x899\x05@8D\xba\x13\x1b\xf5\x11@\x0c\xd0\xe2\x95\x80\x93\x16@\xe2\x95X\x12\xd8\x13\x1a@\xe6Yu|\xd0`\x1c@\xc8\xa3h\x9e\x1c\x94\x1e@\xdcVI\x80\xb9\xb5\x1e@\xe6\xe1\x07\xcaK\x82\x1c@G\x1d\x81\x85\xd0\xbd\x1c@\xa1\xce\x95\x87e\xec\x1b@\x9e"\x88\x91\xab\x90\x1a@\x02!\x9f \xef\xf7\xef?\xf6\xa1l\xc5\xafG\xf0?\xb3\xf6\xef\x14\xfc5\xf3?\x8e|x2\x9bj\xf0?j+\x01B\xa3\xb9\xf2?V\xcc\xc6i\\\x07\xf1?\xbf\xd6S\xde\x15\xdb\xf1?B\xcc\xf6\xd9\xc6z\xf0?\x88\xc1\xa0~\xcco\xed?$Uv_\x94\xe8\xe2?\x82\xd7V\x9f\x8f\xc5\xdc?\x1f\xa5;\x85\xb9O\xe4?\xf0X*\xe7P\xd8\xe1?\xdb+\x1c\x9c\xa0(\xed?A\x8f\xc5e\xb5\xf7\xe7?\x9c,7\t\x84\x87!\xc0\x14\xaa9k\xca\xd6\x18\xc0\xc8\x82\xe1D\x9d\xfa\x10\xc0\x82\xc4\xe5\x0e:E\x04\xc0\xfc\xbf\xc7\x0c\xc5\xd5\xf6\xbfP\x86\xbf\xd5]K\xdf\xbf@{D\xfb(:\xce? 0\xd2\xd0\xecv\xe3?(\xca\x1a\xb9\x06\xa3\xea?\xd8\xb11\xa7L~\xf1?\xc81\x0f\x86\x82v\xe5?\x94\xbd\xa5\xce\xa1.\xee?\x80\xef$\xe0h\xeb\xf4?K\xe5$\'\xf9\xf5\xf5?6\xb9\xc2\xdc\x9ev\xf6?t\xc3\xd2\x16ZZ\xf0?\x94q\xff@\xa5\xd4\xf3?W0\xed\x1a\x96N\xf4?\x90y4fk\x8d\xf4?\x1e\x8c\xed\xb6O\xd7\xf2?\xa4\x17\xdcJv_\xf3?\xfd\xe7\xff\xbb#P\xf3?\x80\xcbD\x16\xc6\x8f\xe0?d/*\x1f\xf5\xba\xe2? \x96\x86\x16\x0b\x9b\xdc?\xae\xbf\xc4Vm}\xe0?\x8b\x0e/\x15\x87\xb9\xe0?tU(c\xa3\x92\xe2?\xf9\xbet\xedd\x05\xf1?\xf8\xb5\xeb\x03\x03,\xed?\\\x01\xcd\xd3h\xc2\xd8\xbf\xb0w\x04\x91\xf3\xb8\xb6\xbf\x00\xe3B^\x03\xcf\x83?P\x10\xe5,O\xee\xb7? ^\x9e\xdct\xbf\xcb?\x90\x98=u\x9aD\xc7?\xf0QYc\x94\x86\xb8?\xd8\x87\x02\x81\xf4I\xc2?\x90?$jU\x14\xd1?\xdeIs&\xf7\xe1\xd4?D9\xee9\xc7\x07\xcb?\xe6M\xf5:\xa7\x84\xd3?\xe0\nv\x97\xaf\x18\xe4?\r\x9c\xf8\x97\xba\xdc\xe1?\x989\xe1\xf4\x96\xe4\xe0?\x00\x1b\xc8\xf0\xe4\x87\xde?,^\x04$\xf4\x1b\xda?p\x08\x8c\xdd\xd9\x97\xd7?\xfd\xb3D0=\x14\xd5?\xe0B\xe6+\x04V\xd5?\xbe\x8dx\x7f\xc6\xf7\xe0?\xc1\x87\x12`\x07~\xd7?\x14\xadB\xa8\xf3$\xff?\xd4:\xf3[u\xb5\xf5?\x82}\x00^.,\xef?\xb0F\x11\xac>\x8c\xe6?\xc0J\xfc\xa1\x03\x9c\xdd?\x90\\E\xe5\x05\'\xce?h)\x95\x9a|\xe9\xb5?P\x13ar\x88\x92\xa9\xbf@\x93\xdd\xb0iF\xbe?\x00?\x14\xa4\xe3 \x84\xbf\xac\xea\xf7\xed\x91D\xc3\xbfD7\'\xdf\xab\xaa\xe4? \x8e\xe2\xb9\x87\x9d\xb3?\xc0\xb2}\xbf\xfd \x95\xbf'   # noqa #E501
g_t2 = b'&\xec\x1b\xc9\xee\x0b\xff?)\x9es\x15\x01\xff\x02@D\xec\xda\x93\x9ey\x05@4\xee1\x83s\xfc\x04@U\xaa\x1e\xd4\xc2\xfb\x04@Z\xd2\x08\xb1Q\x93\x05@\xef\x81L_uB\x06@\x1d\xa95\xfc\xee\xb5\x05@\x91\x88\xb1\xbe\xa5\xae\x06@g\xaa\x91\x1bn\xa2\x06@\x08\x08\x16h\xff\xbc\x04@\x99\xa6\xcf6\xc5\xab\x00@\x10\xdc\xcb\x1cq\x82\xfb?u\x91fh\x1e\xe6\xf4?\x97\x01\xaa\xa4\x0bu\xf3?7\xac\xf5E\x86\xe1\xf3?\xc7\xa8l\x95\xf8\x86\xf4?\xf0\xa8 z\x10\xc4\xf3?$\xa5k\x1ds\xf1\xfa?y\xf4=\xad\xa2\x0b\xff?\t(\xa4{y\xad\xfe?\xe1\x89\x8d\xe8\x9cW\xff?\xaa\xb5S\xf6\x00\x8e\x02@\x92\xceA\xac6@\x06@\x82\xd1\x1e\xa7%\xdf\x05@|\x894\x0c\xa6\xd0\x05@\x15d6\n\xf6\x01\x05@\x99\xb3KI U\x06@\xfa\xe7\xfa&\x88K\x01@!G\x87|{\xa8\x00@\x9b\x9f\x8e\xbb1\xfd\xfe?\x07\xcf\xfb\x8cJ\xba\xff?\t4)6u\x86\xfb?\xf6\x85 "\x89\xcd\xfb?\x91\xed0\n\xb8I\xfb?h\x9b/\xdfkG\xfb?\x1f\xbd\xa6\xd5\x0c\x84\x00@Z\xa5\x1c3\\:\x04@\nc\xd1\xafbm\x05@2~k\xfeAV\x04@\xfc\xb5\xc7\xcb\x05\x04\x06@[\x02\xd6-M\xec\x07@l\xc5\xb0\xcf+<\x0b@R\xdb\xb4#r\xb8\x07@\x99\xfb\xb0\xa2\xee<\x08@\xd6\x7f\x0b\xed\xe7\x82\x08@:l\x9a\xad\xac\x8d\x07@\x0b\xf0\x84\xa7+t\x03@\x8a \xf2\x100x\x03@\xe2D\'{\xd3F\x05@\x92\x96\xb5}y\xcd\x03@X\xe8\x02\xc2\x7f\xb9\x01@\x84\x8e\x8c\xe4\xeb\xf0\xfb?w\xcb\xd4\x11R\x1c\xfa??\xab1\x06\xb4\x9d\x00@\xf5\x9fz{\x18z\x00@I\xb2\xd6\x8d\xab\xf3\xfb?\xb0y\xea\xe9\xbe\xd2\xf8?z\xb4s\xb0)\xab\xf8?\x9c+\xc5\xe7\xa6\x11\xf8?>\xce\xa7\xf9\xc9(\xfb?\xe4\x8a%_\xb6\'\x00@6\xff\xea s\xec\x03@\xacY+\x86A2\x06@\x8cu@\xd6\xc5\x0f\x03@\xc6\xf6\x97V\xe5\xa3\x03@J+\xc9j^\x04\x03@3m\xffeG\x89\x02@\xe2i\xc5\x7f.\xec\x03@\n_Z<\xe7\xd1\x02@\x8d\xfd\xd6\x1e@h\x02@dWl#\xdf\xd8\x01@\x8d8\x9b\\\x93\xa1\x00@\x97\xd7\x7f\xa9\x0e\x04\x03@\xcd\xc1C\xb00\x18\x03@\xfd#\xb0\xba\x03\x82\x06@\xef\xa6\xe8K\xef\xa4\x06@A\xd5\xec\x06B\x8b\x07@\xe6\xd3\xf1\x0b\xfb\xf5\n@\xab&\x96a\x17\x05\x0b@\x9d\x10\x87\x96\x10\xa9\n@BN\xda\xd5\x01\xa3\x02@\x85T\x8cE\xad\x01\x05@@5d\xe0\xfc\x18\x05@\xf5\xdb\xeaf\xd4@\x00@:\x7fJ5l\x8d\x02@\x8a\xeb\xc7^\x1e)\x02@m\xd8\xb6\xe8J\x84\x01@\xac\x15PM\xd7\x92\xff?\x9d\xc8m\xc7fn\xff?2s\x95\xd4\x9df\xff?\xd7CM\xaf\x92\x9f\x01@Id\xe8uM+\x04@\x10wT\xf6>\xd9\x03@F\xb3\x04\xb6\xd5\x08\x06@4\xafo\xe6\x95\xf0\x03@\xbc\xd4\x1a\x04\xd6\xcd\x04@]\xcam\xc1m \t@K$r\xb2\xc9\x1a\t@\xe4\xe5\xe8\xa3AR\n@\xd9\xc4\xec\xb5\xdd\xf9\n@\xf7\xe1Y\xea{H\x08@^f\'\xe6\xe1\xdb\x05@\x01\xa1:\x19\x96\x90\x06@\x9c\\\xed\xe89\x85\x07@\'\x9e\xf4\xdd\x19\x8c\x07@\x1e%}\x9f\xe2\x15\n@\x1bd~\xad\xf4\xc4\x05@cN"\xad\x8fY\x06@V\x17|2\n[\n@?^3:\xa6K\r@\xaf2\x16hW\x0c\x0e@D\xcc\xef\xf7\x83\x99\x0e@>\xce\xe0\xb2\xc0\xe8\x0e@\xdd\xd82x\\\x02\x0b@\xe7\x97Ya\xac\xed\x0c@\xfb\x1fd2\xea\x00\t@LN\xff3\xa7{\x08@,S\xdfK?y\x08@~\xb7E\x7f+\xdd\x03@\xa77\xdcX\xb1\x95\xff?\xff\xbet\xafW\x8d\xf9?\xb1\x92@\x1f7\x83\x00@\xe7\x9c^\xab\x1d \x00@\xf3\x924\x07l\xe6\x04@\xa4l4\xd6\xfa[\x06@\x1aceu\'X\t@\xff8P\xean\xf5\t@\xebc\xaa\xef\xf4\xbe\x0b@\xb1R?d;-\x0e@\xf1\xbaq#\xdd"\x10@E\x94\xbb\xf3\x12\xd3\x11@\x98c\xaez\xb8\xff\x0f@\x9f\xbe*\xde\x08\xb7\x0e@#\xdfof\xf7\x13\t@\xd0\x15\x91(D\xb8\x06@\x11\x046o\n\x86\x05@\xee\x1e@\x11&\x0c\x02@0\x82}+j\xa1\x03@\xd5$\xcd\x1b\xbe\xa2\x01@&?\xd5&\x97-\x00@\xfb\xebg\x97<m\xf9?D\xc4\xf5\xff\xa5r\xf9?\xc6\xbe\xbf\xef]e\xf9?\x18l\x92e\\\x18\xfb?N \x1e4\xaf\'\xf7?sT\xc6\xd8\xd3[\xfb?\x1f\x94\x1c \x05\xe9\xfa?\xeb\xb0s\r\xb0\xc6\xfb?\r*S\xfb\xc8\x9d\xfc?\xc3\xd7\x18\x91\xa3\xa5\xfd?\x94\x97s\xdc.\x8f\xfe?0K\x8b\xc7\xfc\xbf\x00@\xc1\xd6\x90\xe4qw\x05@|\x8aG\x8c\xa3\xdb\x07@#\x9f6\x95>\xf7\x08@W\xfc\x81\xf3\x979\x07@\x8b\x82\x9b\xa2r \x07@\xb7\x7f\x8f\x85\xab\xe5\x07@\to\x19\xb8\xd9>\x08@!}\xb8\xd8,C\x07@\x8d5\x16\xcb\'u\x06@'   # noqa #E501
g_t3 = b'\x95\x13\xbek\xd1O\xcc?\xf5\xdc\x9cSD\xf6\xc0?&\xb1\xee\xdb\xdcD\xca?\x91\xf4\x90\x17\x87*\xd1?\'\x8b[\xfe\x98\xc4\xe0?S\x84 "\xca\xeb\xe9?\xdd\xea\x80\xd4\xe7\x8c\xeb?\x14@]\xc6\x91\xb2\xe2?\xc8RnQ\xacL\xd9?\xdd-tK\xb8\x03\xe6?\xea\xa9\x81U\x18\x9e\xe4?\xce\xc2\x8f\xa3`\xb0\xdf??\xd4\xb9\x0f0\x89\xeb?\x08\xe7\xe1k\xaay\xe5?\x08\x14:}\xe7.\xe8?\xa4y\x17\xae\xe9j\xda?\xf3\x05\xac:uC\xea?\xab\xf9]B;2\xe0?\'\nYVy\x17\xb6\xbf\x0f\x85<o\xa5\x80\xcb?S\xc4\x00\x95\x86j\xe4?\xd8\xfa\x03\xdc0J\xd5?\xd79\xec[\xb8F\xc9?%s\xed\x94\xfbK\xcc?\x0c\xfa\x91l}\x0e\xe7?)b\x90D\xc4t\xe3?\x87q\x83\x1c\xceM\xe1?~\x13Z\x07\xaf\x08\xd9?\xae\xb6\x0b7$\x1e\xe5?\x0e\xec\x82\xcfe\xcb\xd8?\xd5/p\xdd\xe6>\xe3?\xb8\xa4\xf0\x8c\x0fU\xe9?\xe8-\x9f\xb4&\xd4\xe9?=\x19\xa57\x9b\xba\xa1?~\x12F!\xceU\xdf?\x19\xde\xdb\x85G\x8d\xe4?\x18vO\x0c\xd6\x94\xc5?a\x03\xc1R\x00%\xbb?\xaa\x02\xbc\xa4\x92\xaa\xeb?B.\x0eI\xb9{\xe6?%X\xdf\xc4\xbeR\xd5?\xf5{\x86}\xf1\xa0\xd7?\xee\x16\x05\xfb0\x12\xd3?\xde\xdbF\xea\x1aq\xe1?\x0cT}M8\x8f\xea?\xa6\xf1Ik\xbf\xee\xe8?_\x02\xdaMV\xd1\xd4?G\xcd\xbd\xa2\x0c\xdf\xd8?\x01H\xb1\x9c$e\xea?\xfc\x15\x1a\x86t\x82\xd5?\x94\xc7\xe5\xff\xcb\xea\xe8?]9\x88\t\x1a\xf2\xe3?\xf8\xe7\xb1\x8a\x97\x80\xe5?-\x97\x0b\xbc\x88!\xe4?z\xa4\x12\x0b<u\xc0?\xd2*O\xc3\xa1\xfa\xe3?\xfc\x1d5G\xf9\xa6\xe5??\x10\xcbp^\xc3\xe2?\xe1\x85\xb1\x10\xab\xec\xdf?\x9d$\xd4G\x07\xd4\xbe?\xc6\xbcI\x8c}!\xcd?\n\x8f\xf9\x93Mb\xc9?\xfaV\xb1\x89\xefc\xc5?"eE\x80\n\xbc\xd2?\x97\xdf\x12\xc1\x87\xf5\xe2?(\xcb\x1c%\xde`\xea?)\xac\xe9>\xd1@\xe5?\xb0\x83\xca\xf0Y\xbe\xe2?+\xd7\x1b\x8cmB\xd6?\xc5f\x01T\xfcr\xe2?\xe3x\xcb\x9d5\xd7\xe8?De2\xce\x81R\xd4?\xf4\xe3\x8f\x96\x9f\xb1\xc8?*N\xb7CD\xa4\xb8?h\xcbs%\x1fo\xe6?\xa8\x9d\xff\xd9b\xb9\xc6?\xabpb\xb4\xc5[\xe1?\xdd"U\xb8\xec\xf9\xea?\xcd\xd2\xad:9U\xcb?pk\xceP~\xfc\xe2?\x83\xce.\xd1l`\xe3?\x02\x01\x7fy\xe8\xa2\xc6?F`\x00\xa1\x10\x8b\xd2?*\xcdx\x13\x19\xb3\xe7?\xb6\xff\xf2\xe5E\x81\xe6?\x95\xaf`\xebB\x95\xcf?\xef\xeb\xa7\x7f}\xbf\xe7?\xa2\x86\xd2\xba6\xf2\xdf?\x97\xe6\xb1\x19\xef+\xe1?B\xaef\x9eU.\xdf?\xaeI\x1c)r\x05\xe3?a\xbf\x960\xdc\xdb\xa9?\xd85\x15\x05\x1fm\xbf?\xf0\xe4Q\xeb\xaf>\xe5?1\x07\xb0V\x08/\xd2?\x8c\xdc_\x84F\x17\xe6?\xb0%\xb4\xfd\xbf.\xd8?CE\xca\x8e\x08Q\xcd?\xce\x85Sv+\xf9\xe5?\xc9\xdbP\xc82B\xdd?\x97\x8c\xf4\xdb\xdaN\xe0?\xa2\x18\xe9\x13Gd\xee?\xb0\xeaT\x8djL\xd3?\x1c\xbf\x81\xe78p\xdd?\xe9N\x13\xb2s\x1d\xd0?\xc0y\xdd\x15%i\xe1?\x9b\x1d\xa3\xa9(\xca\xd1?\xdf!\xa0\x93\xb7\xce\xe3?_A}\xb0\xff\xf2\xe9?\xab\xc0\xb0\tq\xb4\xc9?\xb2\xda\xder\xd5\x16\xd3?\xe0Tl\x81\xcc\xba\xd2?\x95\xd8\x94l\x04\x8b\xee?\xa1\xbd\x9a\x0c\xd1\xd2\xec?\x87\x06\xd1\x06\xf4\x07\xe2?E5\n\x90R\xe8\xd6?\x08\x95\x03\x1aK.\xe9?\xc1\x83\xc7\x1d\xcf\n\xe3?\t\x0c{\x94q\xb7\xe5?e\xcaA\xd0\x8b\xa5\xdd?\xc0\\2y\x91\xfe\xe3?\x1b7L\x05\x0c~\xc8?\x00t\x83\x01\x90\x0f\xbc?_\r\xab\x02t\x1a\xe9?\x1a;"V\xf8\xcc\xbe?l\x14\xc2\x0c\\\xca\xc8?\xae\xcb\x85\x8e8\x00\xd2?\xd2\xa9\x93\xbfgZ\xea?\xe1\x19{\t\x0f(\xdb?W\x81^\x89\xa8\x88\xd8?\xd0c\xb3\xf6>\x83\xdc?\x0e\xabQ\xc4\x1c,\xd6?t\x98!\x1d\xa7\xa9\xe1?@M%\xc8\x92\xfd\xea?luH\xbd?8\xe7?\xc4\xb86tT\xb0\xd7?n\xbe\xbb\xa0\xed\x81\xd5?\x1c\xd9e]G:\xe5?\x0e\xed\xe1\xf4K\xe8\xed?Om\xd4\xb1\xffw\xe5?\x01\xb1\x1a\x00\xdb\x90\xe7?\x88\xaa\xdc\x1b\x00\x0e\xd8?K=\x0c\x02\xa9W\xd5?\xb6\xedl#\xa4\xa6\xe6?\x8e\xa4\x84\x05\xdfz\xd5?$\xecR\xc3\x85B\xe0?\xe5b\n\x83@qn?T\x17v\x80h\xdc\xe1?\x1bk<\xfc\x0e\x94\xd0?\x8a\x9b\xab<\x9f\x02\xe9?\xd2\xe7\x86\xef\xf1|\xd4?2\xbb\xf1\xc3X\xac\xe9?\xbe:&\x83\x95a\xd0?\xd3\xdb\xe4R\xed\xd5\xc0?\xeb\x15\xf7bF\xb2\xd2?\xe0\xbdx\xf4.9\xdd?x0\xd0\xe7=&\xd6?\xc3`a8QV\xe6?\x85\xc3\x0b_R\xbb\xd7?\x03y$\xb5c:\xed?B_]\x13~\xa4\xe3?\x1d\x1bh\x8c3I\xe9?'    # noqa #E501


class TestNodes(unittest.TestCase):

    def setUp(self):
        warnings.simplefilter('ignore', category=ImportWarning)
        warnings.simplefilter('ignore', category=DeprecationWarning)
        # ignore importlib warnings.
        size = 200
        half = size // 2
        self.size = size
        self.half = half
        np.random.seed(10)
        random_array = np.random.rand(size)
        open_array = np.random.rand(size)
        close_array = np.random.rand(size)
        high_array = np.random.rand(size)
        low_array = np.random.rand(size)
        volume_array = np.random.rand(size)
        indicator = np.zeros(size, dtype=np.int32)
        indicator[0] = 1
        indicator[half] = 1
        df = cudf.DataFrame()
        df['in'] = random_array
        df['open'] = open_array
        df['close'] = close_array
        df['high'] = high_array
        df['low'] = low_array
        df['volume'] = volume_array
        df['indicator'] = indicator
        df['asset'] = 1
        df['asset'].iloc[half:] = 2
        index = np.array(list(reversed(range(0, size))))
        df.index = index
        gt_index = np.concatenate([index[1:half], index[half+1:]])
        self._cudf_data = df
        self.gt = pd.Series(np.frombuffer(ground_truth, dtype=np.float64),
                            index=gt_index)
        gt_index2 = np.concatenate([index[19:half], index[half+19:]])
        self.gt1 = pd.Series(np.frombuffer(g_t1, dtype=np.float64),
                             index=gt_index2)
        self.gt2 = pd.Series(np.frombuffer(g_t2, dtype=np.float64),
                             index=gt_index2)
        self.gt3 = pd.Series(np.frombuffer(g_t3, dtype=np.float64),
                             index=gt_index2)

    def tearDown(self):
        pass

    @ordered
    def test_return(self):
        '''Test return feature node'''
        conf = {
        }
        node_obj = {"id": "abc",
                    "type": "ReturnFeatureNode",
                    "conf": conf,
                    "inputs": {}}
        task = Task(node_obj)
        inN = ReturnFeatureNode(task)
        o = inN.process({'stock_in': self._cudf_data})['stock_out']
        err, index_err = error_function_index(o['returns'], self.gt)
        msg = "bad error %f\n" % (err,)
        self.assertTrue(np.isclose(err, 0, atol=1e-6), msg)
        msg = "bad error %f\n" % (index_err,)
        self.assertTrue(np.isclose(index_err, 0, atol=1e-6), msg)

    @ordered
    def test_indicator(self):
        '''Test indicator node'''
        conf = {
            "indicators": [
                {"function": "port_chaikin_oscillator",
                 "columns": ["high", "low", "close", "volume"],
                 "args": [10, 20]},
                {"function": "port_bollinger_bands",
                 "columns": ["close"],
                 "args": [10],
                 "outputs": ["b1", "b2"]}
            ],
            "remove_na": True
        }
        node_obj = {"id": "abc",
                    "type": "IndicatorNode",
                    "conf": conf,
                    "inputs": {}}
        task = Task(node_obj)
        inN = IndicatorNode(task)
        o = inN.process({'stock_in': self._cudf_data})['stock_out']
        err, index_err = error_function_index(o['CH_OS_10_20'], self.gt1)
        msg = "bad error %f\n" % (err,)
        self.assertTrue(np.isclose(err, 0, atol=1e-6), msg)
        msg = "bad error %f\n" % (index_err,)
        self.assertTrue(np.isclose(index_err, 0, atol=1e-6), msg)

        err, index_err = error_function_index(o['BO_BA_b1_10'], self.gt2)
        msg = "bad error %f\n" % (err,)
        self.assertTrue(np.isclose(err, 0, atol=1e-6), msg)
        msg = "bad error %f\n" % (index_err,)
        self.assertTrue(np.isclose(index_err, 0, atol=1e-6), msg)

        err, index_err = error_function_index(o['BO_BA_b2_10'], self.gt3)
        msg = "bad error %f\n" % (err,)
        self.assertTrue(np.isclose(err, 0, atol=1e-6), msg)
        msg = "bad error %f\n" % (index_err,)
        self.assertTrue(np.isclose(index_err, 0, atol=1e-6), msg)

    @ordered
    def test_asset_indicator(self):
        '''Test asset indicator node'''
        conf = {
        }
        node_obj = {"id": "abc",
                    "type": "AssetIndicatorNode",
                    "conf": conf,
                    "inputs": {}}
        task = Task(node_obj)
        inN = AssetIndicatorNode(task)

        gt = self._cudf_data.to_pandas()['indicator']
        o = inN.process({'stock_in':
                         self._cudf_data.drop('indicator', axis=1)})['stock_out']

        err, index_err = error_function_index(o['indicator'], gt)
        msg = "bad error %f\n" % (err,)
        self.assertTrue(np.isclose(err, 0, atol=1e-6), msg)
        msg = "bad error %f\n" % (index_err,)
        self.assertTrue(np.isclose(index_err, 0, atol=1e-6), msg)


if __name__ == '__main__':
    unittest.main()
