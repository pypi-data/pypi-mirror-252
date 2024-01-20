# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import csv
import random
from os import rename

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.utils.text import slugify
from django.contrib.auth import authenticate

from sportspicker.models import Club, ClubUser, UserProfile


class Command(BaseCommand):
    help = """Loads Participants from a csv file and creates Club based on parsed file name with Participants"""

    def add_arguments(self, parser):
        parser.add_argument('file_name', nargs='+', type=str)
        parser.add_argument('password_method', nargs='+', type=str)
        parser.add_argument('force_username_change', nargs='+', type=str)
        parser.add_argument('force_password_change', nargs='+', type=str)

    def handle(self, *args, **options):
        file_name = options['file_name'][0]
        csv_write_file_name = (file_name + '.tmp')
        password_method = unicode(options['password_method'][0]).lower()
        force_username_change = str(options['force_username_change'][0]).lower()
        force_password_change = str(options['force_password_change'][0]).lower()
        clubname = self.derive_label_from_file_name(file_name)
        club = (self.add_club_to_contest(clubname))
        if Group.objects.filter(name='Picker').exists() is False:
            group = Group.objects.get_or_create(name='Picker')
            # Code to add permission to group ???
        else:
            group = Group.objects.get(name='Picker')

        csvfieldnames = (
                'ID', 'PSWD', 'FNAME', 'LNAME', 'EXPERT', 'DISABLE', 'ADDRESS', 'CITY', 'STATE', 'ZIP', 'COMPANY',
            )

        with open(file_name) as csvfile:
            reader = csv.DictReader(csvfile)
            csvwritefile = open(csv_write_file_name, 'w')
            writer = csv.DictWriter(csvwritefile, fieldnames=csvfieldnames)
            writer.writeheader()
            for row in reader:
                # this is temporary until we get an export with email addresses
                # ToDo - Split this off into its own method
                expertstring = ''
                try:
                    expertvalue = row['EXPERT'].strip()
                except:
                    expertvalue = 'N'
                if force_username_change == 'yes':
                    username = self.generate_username((row['FNAME']), (row['LNAME']), clubname)
                elif (row['ID']) != "" and (row['ID']) is not None:
                    username = (row['ID']).strip()
                else:
                    username = self.generate_username((row['FNAME']), (row['LNAME']), clubname)
                if force_password_change == 'yes':
                    password = self.generate_password((row['FNAME']), (row['LNAME']), clubname, method=password_method)
                elif (row['PSWD']) != "" and (row['PSWD']) is not None:
                    password = (row['PSWD'])
                else:
                    password = self.generate_password((row['FNAME']), (row['LNAME']), clubname, method=password_method)
                try:
                    if expertvalue == 'Y':
                        is_expert = True
                        expertstring = ' (Expert)'
                    else:
                        is_expert = False
                except:
                    is_expert = False

                try:
                    if row['NEWSLETTER'].strip() == 'Y':
                        gets_newsletter = True
                    else:
                        gets_newsletter = False
                except:
                    gets_newsletter = False

                try:
                    if row['REP'].strip() == 'Y':
                        is_rep = True
                        expertstring += ' (Player Rep)'
                    else:
                        is_rep = False
                except:
                    is_rep = False

                if not User.objects.filter(username=username).exists():
                    user = User.objects.create_user(username=username, password=password)
                    user.first_name = (row['FNAME']).strip()
                    user.last_name = (row['LNAME']).strip()
                    user.save()
                    user.groups.add(group)
                    clubuser = club.add_member(user, is_rep=is_rep)

                    clubuser.is_rep = is_rep
                    clubuser.is_expert = is_expert
                    clubuser.gets_newsletter = gets_newsletter
                    clubuser.save()

                    user_profile, _ = UserProfile.objects.update_or_create(user_id=user.id, defaults={
                        'address': row['ADDRESS'].strip(),
                        'city': row['CITY'].strip(),
                        'state': row['STATE'].strip(),
                        'zip_code': row['ZIP'].strip(),
                        'company': row['COMPANY'].strip(),
                    })

                    writer.writerow(
                        {
                            'ID': user.username,
                            'PSWD': password,
                            'FNAME': user.first_name,
                            'LNAME': user.last_name,
                            'EXPERT': expertvalue,
                            'DISABLE': 'N',
                            'ADDRESS': user_profile.address,
                            'CITY': user_profile.city,
                            'STATE': user_profile.state,
                            'ZIP': user_profile.zip_code,
                            'COMPANY': user_profile.company,
                        }
                    )
                    print("Added {first_name} {last_name}{expertstring} to {club_name}".format(
                        first_name=user.first_name,
                        last_name=user.last_name,
                        club_name=club.name,
                        expertstring=expertstring
                        ))
                else:

                    user = User.objects.get(username=username)
                    if user.groups.filter(name=group.name).exists() is False:
                        user.groups.add(group)
                    if authenticate(username=username, password=password) is None:
                        user.set_password(password)
                        print("Password for {first_name} {last_name} updated to {password}".format(
                            first_name=user.first_name,
                            last_name=user.last_name,
                            password=password
                        ))
                    clubuser = ClubUser.objects.get(user=user, club=club)
                    user_profile, _ = UserProfile.objects.get_or_create(user_id=user.id, defaults={
                        'address': row['ADDRESS'],
                        'city': row['CITY'],
                        'state': row['STATE'],
                        'zip_code': row['ZIP'],
                        'company': row['COMPANY'],
                    })
                    if is_rep != clubuser.is_rep:
                        clubuser.is_rep = is_rep
                    if is_expert != clubuser.is_expert:
                        clubuser.is_expert = is_expert

                    clubuser.save_from_command_line()

                    writer.writerow(
                        {
                            'ID': user.username,
                            'PSWD': password,
                            'FNAME': user.first_name,
                            'LNAME': user.last_name,
                            'EXPERT': expertvalue,
                            'DISABLE': 'N',
                            'ADDRESS': clubuser.address,
                            'CITY': clubuser.city,
                            'STATE': clubuser.state,
                            'ZIP': clubuser.zip_code,
                            'COMPANY': clubuser.company,
                        }
                    )

                    print("Duplicate {first_name} {last_name}{expertstring} already exists in {club_name}".format(
                        first_name=row['FNAME'],
                        last_name=row['LNAME'],
                        club_name=club.name,
                        expertstring=expertstring
                    ))

        rename(file_name, file_name + '.bak')
        rename(csv_write_file_name, file_name)

    @classmethod
    def derive_label_from_file_name(cls, file_name):
        try:
            file_name = (((file_name.split('/'))[-1]).split('.')[0]).replace('-', ' ')
            file_name = file_name.replace(' games', '')
            return file_name
        except:
            return file_name

    @classmethod
    def add_club_to_contest(cls, name):
        club, created = Club.objects.get_or_create(
            name=name, slug=(slugify(name))
        )
        return club

    @classmethod
    def generate_username(cls, fname, lname, cname):
        out = str(fname).strip() + str(lname).strip()
        out = out.replace('.', '')
        out += '@' + cname + '.club'
        out = out.replace(' ', '')
        out = out.lower()
        return out

    @classmethod
    def generate_password(cls, fname, lname, cname, method='random_int'):

        def random_int(lower=10000, upper=99999):
            out = str(random.randint(lower, upper))
            return out

        def last_name(lname):
            out = str(lname).strip()
            out = out.replace(' ', '')
            out = out.replace('.', '')
            out = out.replace(',', '')
            out = out.lower()
            return out

        if method == 'random_int':
            return random_int()

        elif method == 'last_name':
            return last_name(lname)
