#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#include "/media/jmaxime/data-a/tal-projet/build/include/eccodes.h" //"/home/kevin/build/include/eccodes.h"

/*
 * Fonctions utilitaires
 */

long convert_date_format(char date[])
{
    char *temp, *curdate;
    long ldate = 0;

    long jour = strtol(date, &temp, 10);
    curdate = temp;
    curdate++;
    long mois = strtol(curdate, &temp, 10);
    curdate = temp;
    curdate++;
    long annee = strtol(curdate, &temp, 10);

    ldate = annee * 100 + mois;
    ldate = ldate * 100 + jour;

    return ldate;
}

long convert_time_format(char time[])
{
    char *temp, *curtime;
    long ltime = 0;

    ltime = strtol(time, &temp, 10);
    curtime = temp;
    curtime++;
    ltime *= 100;
    ltime += strtol(curtime, &temp, 10);

    return ltime;
}

grib_handle *get_handle_from_date(char *filename, long date, long time, char param)
{
    int err = 0, msgCount = 0, i;
    FILE *in = NULL;
    grib_handle *h = NULL;
    long currentDate, currentTime, currentParam, lparam;

    if (param == 'u')
    {
        lparam = 33;
    }
    else
    {
        lparam = 34;
    }

    in = fopen(filename, "r");
    if (!in)
    {
        printf("ERROR: unable to open file %s\n", filename);
        exit(1);
    }

    GRIB_CHECK(grib_count_in_file(0, in, &msgCount), 0);

    for (i = 0; i < msgCount; i++)
    {
        h = grib_handle_new_from_file(0, in, &err);

        GRIB_CHECK(grib_get_long(h, "time.validityDate", &currentDate), 0);
        GRIB_CHECK(grib_get_long(h, "time.validityTime", &currentTime), 0);
        GRIB_CHECK(grib_get_long(h, "indicatorOfParameter", &currentParam), 0);

        if (currentDate == date && currentTime == time && currentParam == lparam)
        {
            break;
        }

        grib_handle_delete(h);
    }

    fclose(in);

    return h;
}

int get_nearest_point(grib_handle *h, double lat, double lon, double *result)
{

    int err = 0, rslt = 0;
    size_t size = 4;
    grib_nearest *nearest = NULL;
    double lats[4] = {
        0,
    };
    double lons[4] = {
        0,
    };
    double values[4] = {
        0,
    };
    double distances[4] = {
        0,
    };
    int indexes[4] = {
        0,
    };

    nearest = grib_nearest_new(h, &err);

    GRIB_CHECK(rslt = grib_nearest_find(nearest, h, lat, lon, 0, lats, lons, values, distances, indexes, &size), 0);

    result[0] = lats[0];
    result[1] = lons[0];
    result[2] = values[0];

    grib_nearest_delete(nearest);

    return rslt;
}

int set_wind(char *filename, long date, long time, char param, double lat, double lon, double value)
{
    int err = 0, i, j, msgCount = 0, valid = 1;
    double *values = NULL;
    double *latValues = NULL;
    double *lonValues = NULL;
    size_t values_len = 0;
    FILE *in = NULL;
    FILE *out = NULL;
    grib_handle *h = NULL;
    grib_multi_handle *mh = NULL;
    long currentDate, currentTime, currentParam, lparam;

    if (param == 'u')
    {
        lparam = 33;
    }
    else
    {
        lparam = 34;
    }

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

    /* Append all message in the multi handle */
    for (i = 0; i < msgCount; i++)
    {
        /* create new handle from file */
        h = grib_handle_new_from_file(0, in, &err);
        if (h == NULL)
        {
            printf("Error: unable to create handle from file %s\n", filename);
            exit(1);
        }

        GRIB_CHECK(grib_get_long(h, "time.validityDate", &currentDate), 0);
        GRIB_CHECK(grib_get_long(h, "time.validityTime", &currentTime), 0);
        GRIB_CHECK(grib_get_long(h, "indicatorOfParameter", &currentParam), 0);

        /* check if it's the message needed to be modified */
        if (currentDate == date && currentTime == time && currentParam == lparam)
        {
            GRIB_CHECK(grib_get_size(h, "values", &values_len), 0);

            values = (double *)malloc(values_len * sizeof(double));
            latValues = (double *)malloc(values_len * sizeof(double));
            lonValues = (double *)malloc(values_len * sizeof(double));

            GRIB_CHECK(grib_get_double_array(h, "values", values, &values_len), 0);
            GRIB_CHECK(grib_get_double_array(h, "latitudes", latValues, &values_len), 0);
            GRIB_CHECK(grib_get_double_array(h, "longitudes", lonValues, &values_len), 0);

            for (j = 0; j < values_len; j++)
            {
                if (fabs(lat - latValues[j]) < 0.0001 && fabs(lon - lonValues[j]) < 0.0001)
                {
                    values[j] = value;
                    valid = 0;
                    break;
                }
            }
            GRIB_CHECK(grib_set_double_array(h, "values", values, values_len), 0);
        }

        grib_multi_handle_append(h, 0, mh);
    }

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
    free(values);
    grib_handle_delete(h);
    grib_multi_handle_delete(mh);

    return valid;
}

double calcul_wind_speed(double u, double v)
{
    return sqrt((u * u) + (v * v)); // m/s
}

int calcul_wind_angle(double u, double v)
{
    double pi = 3.14159265358979323846;
	return (int)(270 - atan2(v,u) * 180 / pi) % 360;
}
