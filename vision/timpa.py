import cv2
import numpy as np

# fungsi meletakkan gambar BGRA di atas gambar BGR beda ukuran
def timpa(depan, belakang, posisi):
  '''gambar depan BGRA, gambar belakang BGR, posisi [y,x,maxwidth]'''
  [ay, ax, am] = posisi
  scale = am / depan.shape[1]
  depan = cv2.resize(depan, None, fx=scale, fy=scale)
  ah, aw, ac = depan.shape
  if ac == 3:
    depan = cv2.cvtColor(depan, cv2.COLOR_BGR2BGRA)
  elif ac == 1:
    depan = cv2.cvtColor(depan, cv2.COLOR_GRAY2BGRA)
  bh, bw = belakang.shape[:2]
  y0 = int(ay - ah/2)
  x0 = int(ax - aw/2)
  ly0 = max(-y0, 0)
  lx0 = max(-x0, 0)
  ly1 = ly0 + bh
  lx1 = lx0 + bw
  iy0 = ly0 + y0
  ix0 = lx0 + x0
  fy0 = min(y0, 0)
  fx0 = min(x0, 0)
  fy1 = max(y0 + ah, bh)
  fx1 = max(x0 + aw, bw)
  fh = fy1 - fy0
  fw = fx1 - fx0
  bgr = np.zeros([fh, fw, 3], np.uint8)
  bgra = np.zeros([fh, fw, 4], np.uint8)
  bgr[ly0 : ly1, lx0 : lx1] = belakang
  bgra[iy0 : iy0 + ah, ix0 : ix0 + aw] = depan
  alpha = np.float16( cv2.cvtColor(bgra[:,:,3], cv2.COLOR_GRAY2BGR) )
  bingkai = np.uint8( alpha * bgra[:,:,:3] / 255 + (255 - alpha) * bgr / 255 )
  return bingkai[ly0:ly1, lx0:lx1]