import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from main import compute
assert compute(2, 3) == 3, 'compute(2,3) violates the specified maximum'
