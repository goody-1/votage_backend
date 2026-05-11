for app in members pastors connect_groups services attendance events growth_track
do
    python manage.py startapp $app apps/$app
done
