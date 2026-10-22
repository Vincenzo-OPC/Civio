"""B3: independently recompute all 59 baseline Numerical keys (Basic operations 31, Number sequence 28). Run from repo root."""
import json,csv,math
from fractions import Fraction as F
q={x['id']:x for x in json.load(open('docs/research/audit/data/baseline-550-2026-10-17.json'))}
def fib(s):return s[-1]+s[-2]
def d(s):a=[b-c for c,b in zip(s,s[1:])];return s[-1]+a[-1]+(a[-1]-a[-2])
def r(s):return s[-1]*s[-1]/s[-2]
def sq(s):n=round(math.isqrt(int(s[-1])))+1;return n*n
C={41:15+27,42:96/8,43:7*9,44:100-37,45:15,46:80,47:d([2,5,10,17]),173:F(18,100)*450,174:F(3,4)+F(2,3),175:F(125)*F('0.8'),176:2**5,177:3800,178:math.lcm(6,8),179:math.gcd(36,54),180:F('0.125'),181:F(60,200)*100,182:15-3*4+6,183:F(3,8),184:F('2.5')/100*800,
185:36,186:80,187:fib([5,8]),188:r([F(9),F(3)]),189:d([12,20,30]),190:112,191:31*2+1,192:d([95,85,70]),193:36,194:d([5,8,12]),195:r([F(16),F(8)]),196:29,262:F(7,8)*64,263:math.isqrt(196),264:F('3.5')*60,265:F(180)/F('1.2'),266:d([13,16,20]),267:24*5,268:49,
339:48/6+7*2,340:F(15,100)*240,341:F(3,5)*250,342:F('2.75')+F('1.6'),343:800*F('0.9'),344:64,345:d([10,17,26]),346:1,347:34*2-2,348:25,485:84/7+6*3,486:F(18,100)*250,487:F(7,8)*64,488:F('6.4')-F('2.75'),489:1500*F('0.88'),490:33*2-1,491:d([6,12,20]),492:6,493:48,540:7*8-15,541:d([90,75,55])}
NOTE={187:'Fibonacci',191:'x2+1',196:'consecutive primes',267:'factorial (x2,x3,x4,x5)',347:'x2-2',490:'x2-1',176:'power',177:'rounding',178:'LCM',179:'GCF',263:'sqrt'}
def val(o):
  o=o.replace(',','').replace('%','').strip()
  try:return F(o)
  except: return None
rows=[];bad=[]
for i,c in C.items():
  x=q[i];c=F(c);opts=[val(o) for o in x['options']];hits=[k for k,v in enumerate(opts) if v==c]
  ok=hits==[x['correct_option']];rows.append([i,x['sub'],x['stem'],x['options'][x['correct_option']],str(c),NOTE.get(i,''),ok,hits,[o for o,v in zip(x['options'],opts) if v is None]])
  if not ok:bad.append(i)
assert set(C)=={k for k,x in q.items() if x['sub'] in('Basic operations','Number sequence')}
with open('docs/research/audit/data/baseline-b3-numerical-keys-2026-10-18.csv','w',newline='') as f:
  w=csv.writer(f);w.writerow(['id','sub','stem','stored_key','independent_answer','rule','key_matches_unique_option','matching_option_idx','malformed_options']);w.writerows(rows)
print(len(rows),'checked; mismatches',bad);print('malformed',[(r[0],r[8]) for r in rows if r[8]])
