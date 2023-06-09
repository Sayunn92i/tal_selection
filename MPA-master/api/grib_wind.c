#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

#include "grib_wind.h"
#include "grib_wind_tools.h"
#include "/bin/eccodes/include/eccodes.h"

int set_wind_u(char *filename, char *date, char *time, int lat, int lon, double value_u)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *h;
    double nearest[3] = {
        0,
    };

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    h = get_handle_from_date(filename, ldate, ltime, 'u');

    get_nearest_point(h, lat, lon, nearest);

    ret = set_wind(filename, ldate, ltime, 'u', nearest[0], nearest[1], value_u);

    grib_handle_delete(h);

    return ret;
}

int set_wind_v(char *filename, char *date, char *time, int lat, int lon, double value_v)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *h;
    double nearest[3] = {
        0,
    };

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    h = get_handle_from_date(filename, ldate, ltime, 'v');

    get_nearest_point(h, lat, lon, nearest);

    ret = set_wind(filename, ldate, ltime, 'v', nearest[0], nearest[1], value_v);

    grib_handle_delete(h);

    return ret;
}

int set_wind_speed(char *filename, char *date, char *time, int lat, int lon, double value)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *hu, *hv;
    double nearest_u[3] = {
        0,
    };
    double nearest_v[3] = {
        0,
    };
    double new_u, new_v;
    int angle;

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    hu = get_handle_from_date(filename, ldate, ltime, 'u');
    hv = get_handle_from_date(filename, ldate, ltime, 'v');

    get_nearest_point(hu, lat, lon, nearest_u);
    get_nearest_point(hv, lat, lon, nearest_v);

    angle = calcul_wind_angle(nearest_u[2], nearest_v[2]);

    new_u = -value * sin(angle * PI / 180);
    new_v = -value * cos(angle * PI / 180);

    ret += set_wind(filename, ldate, ltime, 'u', nearest_u[0], nearest_u[1], new_u);
    ret += set_wind(filename, ldate, ltime, 'v', nearest_v[0], nearest_v[1], new_v);

    grib_handle_delete(hu);
    grib_handle_delete(hv);

    return ret;
}

int set_wind_dir(char *filename, char *date, char *time, int lat, int lon, int value)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *hu, *hv;
    double nearest_u[3] = {
        0,
    };
    double nearest_v[3] = {
        0,
    };
    double speed, new_u, new_v;

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    hu = get_handle_from_date(filename, ldate, ltime, 'u');
    hv = get_handle_from_date(filename, ldate, ltime, 'v');

    get_nearest_point(hu, lat, lon, nearest_u);
    get_nearest_point(hv, lat, lon, nearest_v);

    speed = calcul_wind_speed(nearest_u[2], nearest_v[2]);

    new_u = -speed * sin(value % 360 * PI / 180);
    new_v = -speed * cos(value % 360 * PI / 180);

    ret += set_wind(filename, ldate, ltime, 'u', nearest_u[0], nearest_u[1], new_u);
    ret += set_wind(filename, ldate, ltime, 'v', nearest_v[0], nearest_v[1], new_v);

    grib_handle_delete(hu);
    grib_handle_delete(hv);

    return ret;
}

int set_wind_speed_percentage(char *filename, char *date, char *time, int lat, int lon, double percentage)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *hu, *hv;
    double nearest_u[3] = {
        0,
    };
    double nearest_v[3] = {
        0,
    };
    double speed, new_speed, new_u, new_v;
    int angle;

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    hu = get_handle_from_date(filename, ldate, ltime, 'u');
    hv = get_handle_from_date(filename, ldate, ltime, 'v');

    get_nearest_point(hu, lat, lon, nearest_u);
    get_nearest_point(hv, lat, lon, nearest_v);

    speed = calcul_wind_speed(nearest_u[2], nearest_v[2]);
    angle = calcul_wind_angle(nearest_u[2], nearest_v[2]);

    new_speed = speed + (speed * percentage / 100);

    new_u = -new_speed * sin(angle * PI / 180);
    new_v = -new_speed * cos(angle * PI / 180);

    ret += set_wind(filename, ldate, ltime, 'u', nearest_u[0], nearest_u[1], new_u);
    ret += set_wind(filename, ldate, ltime, 'v', nearest_v[0], nearest_v[1], new_v);

    grib_handle_delete(hu);
    grib_handle_delete(hv);

    return ret;
}

int set_wind_speed_offset(char *filename, char *date, char *time, int lat, int lon, double offset)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *hu, *hv;
    double nearest_u[3] = {
        0,
    };
    double nearest_v[3] = {
        0,
    };
    double speed, new_speed, new_u, new_v;
    int angle;

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    hu = get_handle_from_date(filename, ldate, ltime, 'u');
    hv = get_handle_from_date(filename, ldate, ltime, 'v');

    get_nearest_point(hu, lat, lon, nearest_u);
    get_nearest_point(hv, lat, lon, nearest_v);

    speed = calcul_wind_speed(nearest_u[2], nearest_v[2]);
    angle = calcul_wind_angle(nearest_u[2], nearest_v[2]);

    new_speed = speed + offset;

    if (new_speed > 0)
    {
        new_u = -new_speed * sin(angle * PI / 180);
        new_v = -new_speed * cos(angle * PI / 180);

        ret += set_wind(filename, ldate, ltime, 'u', nearest_u[0], nearest_u[1], new_u);
        ret += set_wind(filename, ldate, ltime, 'v', nearest_v[0], nearest_v[1], new_v);
    }
    else
    {
        ret = 1;
    }

    grib_handle_delete(hu);
    grib_handle_delete(hv);

    return ret;
}

int set_wind_dir_offset(char *filename, char *date, char *time, int lat, int lon, int offset)
{
    int ret = 0;
    long ldate, ltime;
    grib_handle *hu, *hv;
    double nearest_u[3] = {
        0,
    };
    double nearest_v[3] = {
        0,
    };
    double speed, new_u, new_v;
    int angle, new_angle;

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);

    hu = get_handle_from_date(filename, ldate, ltime, 'u');
    hv = get_handle_from_date(filename, ldate, ltime, 'v');

    get_nearest_point(hu, lat, lon, nearest_u);
    get_nearest_point(hv, lat, lon, nearest_v);

    speed = calcul_wind_speed(nearest_u[2], nearest_v[2]);
    angle = calcul_wind_angle(nearest_u[2], nearest_v[2]);

    new_angle = (angle + offset) % 360;

    new_u = -speed * sin(new_angle * PI / 180);
    new_v = -speed * cos(new_angle * PI / 180);

    ret += set_wind(filename, ldate, ltime, 'u', nearest_u[0], nearest_u[1], new_u);
    ret += set_wind(filename, ldate, ltime, 'v', nearest_v[0], nearest_v[1], new_v);

    grib_handle_delete(hu);
    grib_handle_delete(hv);

    return ret;
}

int set_wind_area_generic(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, val_type_t val_type, bool is_offset, double value)
{
    int i, j, msgCount = 0, err = 0, ret = 0;

    long ldate, ltime;
    size_t values_len;
    double *u_values = NULL, *v_values = NULL;
    double *latValues = NULL;
    double *lonValues = NULL;
    FILE *in = NULL;
    FILE *out = NULL;
    grib_handle *h = NULL, *hu = NULL, *hv = NULL;
    grib_multi_handle *mh = NULL;
    long currentDate, currentTime;
    double speed, new_speed, new_angle;

    ldate = convert_date_format(date);
    ltime = convert_time_format(time);
    /* Open grib file */
    in = fopen(filename, "r");
    if (!in)
    {
        printf("ERROR: unable to open file %s\n", filename);
        exit(1);
    }

    /* Count the number of message in the file */
    GRIB_CHECK(grib_count_in_file(0, in, &msgCount), 0);

    /* Creating a multi handle */
    mh = grib_multi_handle_new(0);
    if (!mh)
    {
        printf("unable to create multi field handle\n");
        exit(1);
    }

    // get hu and hv
    for (i = 0; i < msgCount; i++)
    {
        h = grib_handle_new_from_file(NULL, in, &err);
        if (h == NULL)
        {
            printf("Error: unable to create handle from file %s (%d,i=%d)\n", filename, err, i);
            exit(1);
        }

        GRIB_CHECK(grib_get_long(h, "time.validityDate", &currentDate), 0);
        GRIB_CHECK(grib_get_long(h, "time.validityTime", &currentTime), 0);

        if (currentDate == ldate && currentTime == ltime)
        {
            hu = h;
            hv = grib_handle_new_from_file(0, in, &err);
            i++;
            // next is always the v value, u is always first

            GRIB_CHECK(grib_get_size(hu, "values", &values_len), 0);

            u_values = (double *)malloc(values_len * sizeof(double));
            v_values = (double *)malloc(values_len * sizeof(double));
            latValues = (double *)malloc(values_len * sizeof(double));
            lonValues = (double *)malloc(values_len * sizeof(double));

            GRIB_CHECK(grib_get_double_array(hu, "values", u_values, &values_len), 0);
            GRIB_CHECK(grib_get_double_array(hv, "values", v_values, &values_len), 0);
            GRIB_CHECK(grib_get_double_array(hu, "latitudes", latValues, &values_len), 0);
            GRIB_CHECK(grib_get_double_array(hu, "longitudes", lonValues, &values_len), 0);
            for (j = 0; j < values_len; j++)
            {

                if (latValues[j] < min_lat && latValues[j] > max_lat && lonValues[j] < min_lon && lonValues[j] > max_lon)
                {

                    switch (val_type)
                    {
                    case VAL_ANGLE:
                        if (is_offset)
                        {
                            speed = calcul_wind_speed(u_values[j], v_values[j]);
                            new_angle = atan2(v_values[j], u_values[j]) - value * PI / 180;
                            u_values[j] = speed * cos(new_angle);
                            v_values[j] = speed * sin(new_angle);
                        }
                        else
                        {
                            speed = calcul_wind_speed(u_values[j], v_values[j]);
                            new_angle = (270 - value) * PI / 180;
                            u_values[j] = speed * cos(new_angle);
                            v_values[j] = speed * sin(new_angle);
                        }
                        break;
                    case VAL_SPEED:
                        if (is_offset)
                        {
                            speed = calcul_wind_speed(u_values[j], v_values[j]);
                            new_speed = speed + value * 0.514444;

                            if (new_speed <= 0)
                            {
								new_speed = 0.514444;
                            }
							u_values[j] = u_values[j] * new_speed / speed;
                            v_values[j] = v_values[j] * new_speed / speed;
                        }
                        else
                        {
                            speed = calcul_wind_speed(u_values[j], v_values[j]);
                            new_speed = value * 0.514444;

                            if (new_speed <= 0)
                            {
								new_speed = 0.514444;
                            }
							u_values[j] = u_values[j] * new_speed / speed;
                            v_values[j] = v_values[j] * new_speed / speed;
                        }
                        break;
                    case VAL_POURC:
                        if (is_offset)
                        {
                            speed = calcul_wind_speed(u_values[j], v_values[j]);
                            new_speed = speed + (speed * value / 100);

                            if (new_speed <= 0)
                            {
								new_speed = 0.514444;
                            }
							u_values[j] = u_values[j] * new_speed / speed;
                            v_values[j] = v_values[j] * new_speed / speed;
                        }
                        else
                        {
                            printf("les pourcentages doivent être forcément des offset\n");
                        }
                        break;
                    }
                }
            }

            GRIB_CHECK(grib_set_double_array(hu, "values", u_values, values_len), 0);
            GRIB_CHECK(grib_set_double_array(hv, "values", v_values, values_len), 0);

            // append both hu and hv to mh
            grib_multi_handle_append(hu, 0, mh);
            grib_multi_handle_append(hv, 0, mh);
        }
        else
        {
            grib_multi_handle_append(h, 0, mh);
        }
    }
    // write to output file
    fclose(in);
    /* open output file */
    out = fopen(filename, "w");
    if (!out)
    {
        printf("ERROR: unable to open file %s\n", filename);
        exit(1);
    }

    /* write multi fields handle to output file */
    grib_multi_handle_write(mh, out);

    fclose(out);
    free(latValues);
    free(lonValues);
    free(u_values);
    free(v_values);
    grib_handle_delete(h);
    grib_handle_delete(hu);
    grib_handle_delete(hv);
    grib_multi_handle_delete(mh);

    return ret;
}
