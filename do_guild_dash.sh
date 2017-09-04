usage()
{
cat << EOF
usage: $0 options

This script executes the SWGOH guild dash python script and puts the processed html into your web root.

OPTIONS:
   -h      Show this message
   -p      Specify the path to the web root to deploy the processed html to (required)
   -n      Specify the name to give the processed html file (required)
EOF
}

while getopts "p:n:h" OPTION
do
  case $OPTION in
    h)
      usage
      exit 1
      ;;
    p)
      WEBPATH=$OPTARG
      ;;
    n)
      PROCESSEDNAME=$OPTARG
      ;;
    ?)
      usage
      exit 1
      ;;
  esac
done

/usr/bin/python3 tbdash.py
mv ./processed_guild.html $WEBPATH/$PROCESSEDNAME
