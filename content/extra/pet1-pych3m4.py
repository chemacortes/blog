n=input();d=1;r=""
while d<n:
 d+=1;s=0
 while n%d<1:n/=d;s+=1
 if s:r+=" x %d"%d+"^%d"%s*(s>1)
print r[3:]or n