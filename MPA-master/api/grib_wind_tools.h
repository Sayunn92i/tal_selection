#ifndef grib_wind_tools_H
#define grib_wind_tools_H

#include "/home/kevin/build/include/eccodes.h"

/*
 * Converti le format d'une date d'une chaine de caractère en un long : dd/mm/yyyy -> yyyymmdd.
 * Ce format correspond a celui utiliser dans les fichiers grib.
 */
long convert_date_format(char date[]);

/*
 * Converti le format d'une heure d'une chaine de caractère en un long : hh:mm:ss -> hhmm.
 * Ce format correspond a celui utiliser dans les fichiers grib.
 * A noter que les secondes sont optionnel, non utilisé dans le fichier grib.
 */
long convert_time_format(char time[]);

/*
 * Permet de récupérer un message précis en mémoire a partir de sa date et de son heure.
 */
grib_handle *get_handle_from_date(char *filename, long date, long time, char param);

/*
 * Prend en paramétre une latitude et une longitude et renvoie le points le plus proche dans un tableau result ainsi que la valeur du point.
 * Le tableau result est renvoyer sous le format suivant : [latitude, longitude, valeur]
 * Cette fonction permet de simplifier la fonctionnalité déja existante mais légérement complexe de grib_api.
 */
int get_nearest_point(grib_handle *h, double lat, double lon, double *result);

/*
 * Pas implémenter
 */
int set_wind(char *filename, long date, long time, char param, double lat, double lon, double value);

/*
 * Calcul du la vitesse du vent en m/s a partir de u et de v.
 */
double calcul_wind_speed(double u, double v);

/*
 * Calcul de l'angle du vent en degrés a partir de u et de v.
 */
int calcul_wind_angle(double u, double v);

#endif
