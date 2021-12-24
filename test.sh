T1="foo"
T2="foo"

echo $T1
echo $T2

if [ "$T1" = "$T2" ]; then
  echo 'equal'
else
  echo 'not equal'
fi
