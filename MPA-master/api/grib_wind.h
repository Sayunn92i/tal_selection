#ifndef grib_wind_H
#define grib_wind_H

#define PI 3.14159265358979323846
#include <stdbool.h>

typedef enum val_type
{
	VAL_ANGLE,
	VAL_SPEED,
	VAL_POURC
} val_type_t;

int set_wind_area_generic(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, val_type_t val_type, bool is_offset, double value);

void get_speed_values(double old_u, double old_v, double *new_u, double *new_v);

int set_wind_u(char *filename, char *date, char *time, int lat, int lon, double value_u);
/* les types spécifiés sont a adapté, je suppose que date (jour/année) et time (hh:mm:ss) peuvent être des chaînes de format fixe, lat la latitude, long la longitude, value_u la valeur de la composante u du vent
Cette fonction récupère le point de la grille le plus proche de (lat, long) et écrase la valeur de la composante u du vent par value_u.*/

int set_wind_v(char *filename, char *date, char *time, int lat, int lon, double value_v);
/* Cette fonction récupère le point de la grille le plus proche de (lat, long) et écrase la valeur de la composante v du vent par value_v.
 */

int set_wind_speed(char *filename, char *date, char *time, int lat, int lon, double value);
/* Cette fonction récupère le point de la grille le plus proche de (lat, long) et change la valeur de la vitesse du vent par value sans modifier sa direction.*/

int set_wind_dir(char *filename, char *date, char *time, int lat, int lon, int value);
/* Cette fonction récupère le point de la grille le plus proche de (lat, long) et change la valeur de la direction du vent par value sans modifier sa vitesse. Prendre value modulo 360. */

int set_wind_speed_percentage(char *filename, char *date, char *time, int lat, int lon, double percentage);
/* Cette fonction récupère le point de la grille le plus proche de (lat, long) et change la valeur de la vitesse du vent en pourcentage.*/

int set_wind_speed_offset(char *filename, char *date, char *time, int lat, int lon, double offset);
/* Cette fonction récupère le point de la grille le plus proche de (lat, long) et ajoute à la valeur de la vitesse du vent la valeur de offset (qui peut être négative, il faut simplement veiller à ce que cette vitesse reste positive).*/

int set_wind_dir_offset(char *filename, char *date, char *time, int lat, int lon, int offset);
/* Cette fonction récupère le point de la grille le plus proche de (lat, long) et ajoute offset à la direction du vent. Faire les calculs modulo 360.*/

int set_wind_u_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, double value_u);
/* idem set_wind_u mais pour tous les points compris dans la zone ((min_lat,min_long);(max_lat, max_long))*/

int set_wind_v_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, double value_v);

int set_wind_speed_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, double value);

int set_wind_dir_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, int value);

int set_wind_speed_percentage_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, double percentage);

int set_wind_speed_offset_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, double offset);

int set_wind_dir_offset_area(char *filename, char *date, char *time, double min_lat, double min_lon, double max_lat, double max_lon, int offset);

#endif
