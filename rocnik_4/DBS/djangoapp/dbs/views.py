from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.http import HttpResponse
from django.db import connection
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from dbs.models import Podanie, Bulletin, Raw, Companies, LikvidatorIssues, KonkurzVyrovnanieIssues, ZnizenieImaniaIssues, KonkurzRestrukturalizaciaActors
from django.db.models import F, Q, Count
from django.contrib.postgres.search import SearchVector
from django.contrib.postgres.search import SearchQuery
from functools import reduce
import pickle


import json
import re 
import math

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("SELECT date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime;")
        row = cursor.fetchone()

    return row


def submissions_table(limit, offset, order, order_type, query):
    with connection.cursor() as cursor:
        if query == "none":
            if order_type == "desc":
                cursor.execute("SELECT id, br_court_name, kind_name, cin, registration_date, corporate_body_name, br_section, br_insertion, text, street, postal_code, city FROM ov.or_podanie_issues ORDER BY "+ order +" DESC NULLS LAST LIMIT %s OFFSET %s;", [limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT id, br_court_name, kind_name, cin, registration_date, corporate_body_name, br_section, br_insertion, text, street, postal_code, city FROM ov.or_podanie_issues ORDER BY "+ order +" ASC NULLS LAST LIMIT %s OFFSET %s;", [limit, offset])
        else:
            if order_type == "desc":
                cursor.execute("SELECT id, br_court_name, kind_name, cin, registration_date, corporate_body_name, br_section, br_insertion, text, street, postal_code, city FROM ov.or_podanie_issues WHERE to_tsvector(corporate_body_name || ' ' || cin::TEXT || ' ' || city) @@ to_tsquery(%s) ORDER BY "+ order +" DESC NULLS LAST LIMIT %s OFFSET %s;", [query, limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT id, br_court_name, kind_name, cin, registration_date, corporate_body_name, br_section, br_insertion, text, street, postal_code, city FROM ov.or_podanie_issues WHERE to_tsvector(corporate_body_name || ' ' || cin::TEXT || ' ' || city) @@ to_tsquery(%s) ORDER BY "+ order +" ASC NULLS LAST LIMIT %s OFFSET %s;", [query, limit, offset])
        row = cursor.fetchall()

    return row


    return row

def companies_table(limit, offset, order, order_type, query, last_gte, last_lte):
    with connection.cursor() as cursor:
        if query == "none" and last_gte == "none" and last_lte == "none":
            if order_type == "desc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies ORDER BY "+ order +" DESC NULLS LAST LIMIT %s OFFSET %s;", [limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies ORDER BY "+ order +" ASC NULLS LAST LIMIT %s OFFSET %s;", [limit, offset])
        elif last_gte == "none" and last_lte == "none":
            if order_type == "desc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) ORDER BY "+ order +" DESC LIMIT %s OFFSET %s;", [query, limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) ORDER BY "+ order +" ASC LIMIT %s OFFSET %s;", [query, limit, offset])
        elif last_gte == "none":
            if order_type == "desc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update <= %s ORDER BY "+ order +" DESC LIMIT %s OFFSET %s;", [query, last_lte, limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update <= %s ORDER BY "+ order +" ASC LIMIT %s OFFSET %s;", [query, last_lte, limit, offset])     
        elif last_lte == "none":
            if order_type == "desc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update >= %s ORDER BY "+ order +" DESC LIMIT %s OFFSET %s;", [query, last_gte, limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update >= %s ORDER BY "+ order +" ASC LIMIT %s OFFSET %s;", [query, last_gte, limit, offset])
        else:
            if order_type == "desc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update <= %s and last_update >= %s ORDER BY "+ order +" DESC LIMIT %s OFFSET %s;", [query, last_lte, last_gte, limit, offset])
            elif order_type == "asc":
                cursor.execute("SELECT cin, name, br_section, address_line, last_update, (SELECT count(*) FROM ov.or_podanie_issues WHERE cin = companies.cin GROUP BY cin) AS or_podanie_issues_count, (SELECT count(*) FROM ov.znizenie_imania_issues WHERE cin = companies.cin GROUP BY cin) AS znizenie_imania_issues_count, (SELECT count(*) FROM ov.likvidator_issues WHERE cin = companies.cin GROUP BY cin) AS likvidator_issues_count, (SELECT count(*) FROM ov.konkurz_vyrovnanie_issues WHERE cin = companies.cin GROUP BY cin) AS konkurz_vyrovnanie_issues_count, (SELECT count(*) FROM ov.konkurz_restrukturalizacia_actors WHERE cin = companies.cin GROUP BY cin) AS konkurz_restrukturalizacia_actors_count FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update <= %s and last_update >= %s ORDER BY "+ order +" ASC LIMIT %s OFFSET %s;", [query, last_lte, last_gte, limit, offset])
        
        row = cursor.fetchall()

    return row

def submissions_insert_in_podanie_table(body, bulletin_id, raw_id):
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO ov.or_podanie_issues (id, br_court_name, kind_name, cin, registration_date, corporate_body_name, br_section, br_insertion, street, postal_code, city, address_line, bulletin_issue_id, raw_issue_id, br_mark, br_court_code, kind_code, text, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, '-', '-', '-', '-', now(), now());", [body ['id'], body['br_court_name'], body['kind_name'], body['cin'], body['registration_date'], body['corporate_body_name'], body['br_section'], body['br_insertion'], body['street'], body['postal_code'], body['city'], body['address_line'], bulletin_id, raw_id])
        row = "imported"

    return row

def submissions_insert_in_raw_table(id, bulletin_id):
    with connection.cursor() as cursor:   
        cursor.execute("INSERT INTO ov.raw_issues(id, file_name, created_at, updated_at, bulletin_issue_id) VALUES (%s, 'file name', now(), now(), %s);", [id, bulletin_id])
        row = "imported"

    return row

def submissions_insert_in_bulletin_table(id, number):
    with connection.cursor() as cursor:
        
        cursor.execute("INSERT INTO ov.bulletin_issues(year, published_at, created_at, updated_at, id, number) VALUES (2021, now(), now(), now(), %s, %s);", [id, number])
        row = "imported"

    return row
def submissions_generate_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ov.or_podanie_issues ORDER BY id DESC LIMIT 1 OFFSET 0;")
        row = cursor.fetchall()

    return row[0][0] + 1

def submissions_delete_podanie(id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM ov.or_podanie_issues WHERE id = %s;", [id])
        row = "executed"

    return row

def submissions_delete_bulletine(id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM ov.bulletin_issues WHERE id = %s;", [id])
        row = "executed"

    return row

def submissions_delete_raw(id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM ov.raw_issues WHERE id = %s;", [id])
        row = "executed"

    return row

def get_bulletin_number_and_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, number FROM ov.bulletin_issues ORDER BY id DESC LIMIT 1 OFFSET 0;")
        row = cursor.fetchall()

    return row

def get_raw_id():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ov.raw_issues ORDER BY id DESC LIMIT 1 OFFSET 0;")
        row = cursor.fetchall()

    return row

def is_id_in_podanie(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id FROM ov.or_podanie_issues WHERE id = %s LIMIT 1 OFFSET 0;", [id])
        row = cursor.fetchall()

    return row


def get_raw_bulletin_id(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT bulletin_issue_id, raw_issue_id FROM ov.or_podanie_issues WHERE id = %s LIMIT 1 OFFSET 0;", [id])
        row = cursor.fetchall()

    return row

def submissions_count():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ov.or_podanie_issues;")
        row = cursor.fetchall()

    return row

def companies_count():
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ov.companies;")
        row = cursor.fetchall()

    return row

def submissions_count_query(query):
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ov.or_podanie_issues WHERE to_tsvector(corporate_body_name::TEXT) @@ to_tsquery(%s) or to_tsvector(cin::TEXT) @@ to_tsquery(%s) or to_tsvector(city::TEXT) @@ to_tsquery(%s);", [query, query, query])
        row = cursor.fetchall()

    return row

def companies_count_query(query, last_gte, last_lte):
    with connection.cursor() as cursor:
        if last_gte == "none" and last_lte == "none":
            cursor.execute("SELECT COUNT(*) FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s);", [query])
        elif last_gte == "none":
            cursor.execute("SELECT COUNT(*) FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update <= %s;", [query, last_lte])
        elif last_lte == "none":
            cursor.execute("SELECT COUNT(*) FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update >= %s;", [query, last_gte])
        else:
            cursor.execute("SELECT COUNT(*) FROM ov.companies WHERE to_tsvector(name || ' ' || address_line::TEXT) @@ to_tsquery(%s) and last_update <= %s and last_update >= %s;", [query, last_lte, last_gte])
        row = cursor.fetchall()

    return row


def index(request):
    outputdata = my_custom_sql()
    output = str(outputdata[0])
    output = re.sub(",", "", output)
    n = json.dumps({ "pgsql": {"uptime": output} }, sort_keys=True, default=str)

    return HttpResponse(n)

@csrf_exempt
def podanie_delete(request, id):
    if len(is_id_in_podanie(id)) > 0:
        bulletin_raw_id = get_raw_bulletin_id(id)
        delete_podanie = submissions_delete_podanie(id)
        delete_raw = submissions_delete_raw(bulletin_raw_id[0][1])
        delete_bulletine = submissions_delete_bulletine(bulletin_raw_id[0][0])
        c = json.dumps({})
        x = json.loads(c)
        response = JsonResponse(x ,safe=False)
        response.status_code = 204
        return response
    else:
        c = json.dumps({})
        x = json.loads(c)
        response = JsonResponse(x ,safe=False)
        response.status_code = 404
        return response


@csrf_exempt
def podanie_view(request):

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        errors = []
        
        new_id = submissions_generate_id()
        
        x = json.loads(body)


        if x['br_court_name'] is None:
            error = {
                        "field" : "br_court_name",
                        "reasons": ["required"]
                    }
            errors.append(error)
        
        if x['kind_name'] is None:
            error = {
                        "field" : "kind_name",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['cin'] is None or not isinstance(x['cin'], int):
            error = {
                        "field" : "cin",
                        "reasons": ["required", "not_number"]
                    }
            errors.append(error)
        if x['registration_date'] is None:
            error = {
                        "field" : "registration_date",
                        "reasons": ["required", "invalid_range"]
                    }
            errors.append(error)
        if x['corporate_body_name'] is None:
            error = {
                        "field" : "corporate_body_name",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['br_section'] is None:
            error = {
                        "field" : "br_section",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['br_insertion'] is None:
            error = {
                        "field" : "br_insertion",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['street'] is None:
            error = {
                        "field" : "street",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['postal_code'] is None:
            error = {
                        "field" : "postal_code",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['city'] is None:
            error = {
                        "field" : "city",
                        "reasons": ["required"]
                    }
            errors.append(error)

        if len(errors) > 0:
            c = json.dumps({"errors": errors})
            output = json.loads(c)
            response = JsonResponse(output, safe=False)
            response.status_code = 422
            return response
        else:
            bulletin_number_and_id = get_bulletin_number_and_id()
            raw_id = get_raw_id()
            new_raw_id = raw_id[0][0] + 1
            new_bulletin_id = bulletin_number_and_id[0][0] + 1
            new_bulletin_number = bulletin_number_and_id[0][1] + 1
            bulletin_issues = submissions_insert_in_bulletin_table(new_bulletin_id, new_bulletin_number)
            raw_issues = submissions_insert_in_raw_table(new_raw_id, new_bulletin_id)
            adress_line = x['street'] + ", "+ x['postal_code'] + " "+ x['city']
            out = json.dumps({
                                "id": new_id,
                                "br_court_name": x['br_court_name'],
                                "kind_name": x['kind_name'],
                                "cin": x['cin'],
                                "registration_date": x['registration_date'],
                                "corporate_body_name": x['corporate_body_name'],
                                "br_section": x['br_section'],
                                "br_insertion": x['br_insertion'],
                                "street": x['street'],
                                "postal_code": x['postal_code'],
                                "city": x['city'],
                                "address_line": adress_line
                                })
            out_final = json.loads(out)
            insert = submissions_insert_in_podanie_table(out_final, new_bulletin_id, new_raw_id)
            response = JsonResponse(out_final, safe=False)
            response.status_code = 201
            return response


    elif request.method == 'GET':

        if request.GET.get('order_by') != None:
            order = str(request.GET.get('order_by'))
    
        else:
            order = "id"

        if request.GET.get('order_type') != None:
            order_type = str(request.GET.get('order_type'))
    
        else:
            order_type = "desc"


        if request.GET.get('per_page') != None:
            paginator_size = int(request.GET.get('per_page'))
    
        else:
            paginator_size = 10
    
        if request.GET.get('page') != None:
            page_num = int(request.GET.get('page'))
        else:
            page_num = 1

        if request.GET.get('query') != None:
            query = request.GET.get('query')
            query = re.sub(" ", "|", query)
        else:
            query = "none"


        if request.GET.get('registration_date_gte') != None:
            reg_gte = request.GET.get('registration_date_gte')
        else:
            reg_gte = "none"
        
        if request.GET.get('registration_date_gte') != None:
            reg_lte = request.GET.get('registration_date_gte')
        else:
            reg_lte = "none"

        offset = paginator_size * (int(page_num) - 1)
        limit = paginator_size
        if query == "none":
            total = submissions_count()
        else:
            total = submissions_count_query(query)
        
        table = submissions_table(limit, offset, order, order_type, query)


        courts = []
        if len(table) < limit:
            limit = len(table)
    
        for i in range(limit):
            court = {
                        "id": int(table[i][0]),
                        "br_court_name": str(table[i][1]),
                        "kind_name": str(table[i][2]),
                        "cin": int(table[i][3]),
                        "registration_date": str(table[i][4]),
                        "corporate_body_name": str(table[i][5]),
                        "br_section": str(table[i][6]),
                        "br_insertion": str(table[i][7]),
                        "text": str(table[i][8]),
                        "street": str(table[i][9]),
                        "postal_code": str(table[i][10]),
                        "city": str(table[i][11])
                    }
            courts.append(court)
        meta = {
            "page": int(page_num),
            "per_page": int(limit),
            "pages": math.ceil(int(total[0][0])/limit),
            "total": int(total[0][0])
        }
        #pagination
        court_paginator = Paginator(courts, paginator_size)
        page = court_paginator.get_page(page_num)
    
        c = json.dumps({"items": courts, "metadata": meta})
        x = json.loads(c)
    
        return JsonResponse(x, safe=False)



@csrf_exempt
def companies_view(request):


    if request.method == 'GET':

        if request.GET.get('order_by') != None:
            order = str(request.GET.get('order_by'))
    
        else:
            order = "cin"

        if request.GET.get('order_type') != None:
            order_type = str(request.GET.get('order_type'))
    
        else:
            order_type = "desc"


        if request.GET.get('per_page') != None:
            paginator_size = int(request.GET.get('per_page'))
    
        else:
            paginator_size = 1
    
        if request.GET.get('page') != None:
            page_num = int(request.GET.get('page'))
        else:
            page_num = 1

        if request.GET.get('query') != None:
            query = request.GET.get('query')
            query = re.sub(" ", "|", query)
        else:
            query = "none"


        if request.GET.get('last_update_gte') != None:
            last_gte = request.GET.get('last_update_gte')
        else:
            last_gte = "none"
        
        if request.GET.get('last_update_lte') != None:
            last_lte = request.GET.get('last_update_lte')
        else:
            last_lte = "none"

        offset = paginator_size * (int(page_num) - 1)
        limit = paginator_size
        if query == "none" and last_gte == "none" and last_lte == "none":
            total = companies_count()
        else:
            total = companies_count_query(query, last_gte, last_lte)
        
        table = companies_table(limit, offset, order, order_type, query, last_gte, last_lte)


        companies = []
        if len(table) < limit:
            limit = len(table)
    
        for i in range(limit):
            company = {
                        "cin": int(table[i][0]),
                        "name": str(table[i][1]),
                        "br_section": str(table[i][2]),
                        "address_line": str(table[i][3]),
                        "last_update": str(table[i][4]),
                        "or_podanie_issues_count": str(table[i][5]),
                        "znizenie_imania_issues_count": str(table[i][6]),
                        "likvidator_issues_count": str(table[i][7]),
                        "konkurz_vyrovnanie_issues_count": str(table[i][8]),
                        "konkurz_restrukturalizacia_actors_count": str(table[i][9])
                    }
            companies.append(company)
        if limit == 0:
            limit = 1
        meta = {
            "page": int(page_num),
            "per_page": int(limit),
            "pages": math.ceil(int(total[0][0])/limit),
            "total": int(total[0][0])
        }
        #pagination
        court_paginator = Paginator(companies, paginator_size)
        page = court_paginator.get_page(page_num)
    
        c = json.dumps({"items": companies, "metadata": meta})
        x = json.loads(c)
    
        return JsonResponse(x, safe=False)


####################################
######      ORM       ##############
####################################

def orm_generate_id():
    result = Podanie.objects.order_by(F("id").desc(nulls_last=True)).values("id").first()
    return result
def get_orm_query(order, order_type, query, limit, offset, gte, lte):
    
    if query == "none" and gte == "none" and lte == "none":
        if order_type == "desc":
            result = Podanie.objects.order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
    
    elif gte == "none" and lte == "none":
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query])).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query])).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
    
    
    elif gte == "none":
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__lte = lte).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__lte = lte).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
    
    elif lte == "none":
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__gte = gte).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__gte = gte).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]

    elif query == "none":
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                registration_date__gte = gte, registration_date__lte = lte).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                registration_date__gte = gte, registration_date__lte = lte).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]

    elif query == "none" and gte == "none":
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                registration_date__gte = gte).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                registration_date__lte = lte).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]

    elif query == "none" and lte == "none":
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                registration_date__gte = gte).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                registration_date__gte = gte).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]

    else:
        if order_type == "desc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__gte = gte, registration_date__lte = lte).order_by(F(order).desc(nulls_last=True)).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
        elif order_type == "asc":
            result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__gte = gte, registration_date__lte = lte).order_by(order).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")[offset:limit]
   
    
    return result

def orm_count(query, gte, lte):
    
    if query == "none" and gte == "none" and lte == "none":
        result = Podanie.objects.count()
    elif gte == "none" and lte == "none":
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query])).count()    
    elif gte == "none":
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__lte = lte).count()
    elif lte == "none":
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__gte = gte).count()
    elif query == "none" and gte == "none":
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
            registration_date__lte = lte).count()
    elif query == "none" and lte == "none":
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
            registration_date__gte = gte).count()
    elif query == "none":
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
            registration_date__gte = gte, registration_date__lte = lte).count()
    else:
        result = Podanie.objects.annotate(search=SearchVector('corporate_body_name') + SearchVector('cin') + SearchVector('city')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), registration_date__gte = gte, registration_date__lte = lte).count()
    return result
def orm_insert_into_bulletin(bulletin_id, number_bulletin):
    bulletin = Bulletin.objects.create(
        year = 2021,
        id = bulletin_id,
        number = number_bulletin
    )

def orm_insert_into_raw(raw_id, bulletin_id):
    raw = Raw.objects.create(
        id = raw_id,
        file_name = 'file name',
        bulletin_issue = bulletin_id
    )

def orm_insert_into_podanie(body, bulletin_id, raw_id):
    podanie = Podanie.objects.create(
        id = body ['id'], 
        br_court_name = body['br_court_name'],
        kind_name = body['kind_name'],
        cin = body['cin'],
        registration_date = body['registration_date'],
        corporate_body_name = body['corporate_body_name'],
        br_section = body['br_section'],
        br_insertion = body['br_insertion'],
        street = body['street'],
        postal_code = body['postal_code'],
        city = body['city'],
        address_line = body['address_line'],
        bulletin_issue = bulletin_id,
        raw_issue = raw_id
    )


def orm_get_bulletin_number():
    result = Bulletin.objects.order_by(F("number").desc(nulls_last=True)).values("number").first()
    return result

def orm_get_bulletin_id():
    result = Bulletin.objects.order_by(F("id").desc(nulls_last=True)).values("id").first()
    return result

def orm_get_raw_id():
    result = Raw.objects.order_by(F("id").desc(nulls_last=True)).values("id").first()
    return result


@csrf_exempt
def orm_podanie_view(request):

    if request.method == 'POST':
        body = request.body.decode('utf-8')
        errors = []
        
        new_id = submissions_generate_id()
        new_id += 1

        x = json.loads(body)


        if x['br_court_name'] is None:
            error = {
                        "field" : "br_court_name",
                        "reasons": ["required"]
                    }
            errors.append(error)
        
        if x['kind_name'] is None:
            error = {
                        "field" : "kind_name",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['cin'] is None or not isinstance(x['cin'], int):
            error = {
                        "field" : "cin",
                        "reasons": ["required", "not_number"]
                    }
            errors.append(error)
        if x['registration_date'] is None:
            error = {
                        "field" : "registration_date",
                        "reasons": ["required", "invalid_range"]
                    }
            errors.append(error)
        if x['corporate_body_name'] is None:
            error = {
                        "field" : "corporate_body_name",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['br_section'] is None:
            error = {
                        "field" : "br_section",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['br_insertion'] is None:
            error = {
                        "field" : "br_insertion",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['street'] is None:
            error = {
                        "field" : "street",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['postal_code'] is None:
            error = {
                        "field" : "postal_code",
                        "reasons": ["required"]
                    }
            errors.append(error)
        if x['city'] is None:
            error = {
                        "field" : "city",
                        "reasons": ["required"]
                    }
            errors.append(error)

        if len(errors) > 0:
            c = json.dumps({"errors": errors})
            output = json.loads(c)
            response = JsonResponse(output, safe=False)
            response.status_code = 422
            return response
        else:
            bulletin_number = orm_get_bulletin_number()
            raw_id = orm_get_raw_id()
            bulletin_id = orm_get_bulletin_id()
            new_bulletin_id = bulletin_id["id"] + 1
            new_bulletin_number = bulletin_number["number"] + 1
            new_raw_id = raw_id["id"] + 1
            bulletin_issues = orm_insert_into_bulletin(new_bulletin_id, new_bulletin_number)
            new_bulletin_id = Bulletin.objects.get(id = new_bulletin_id)
            raw_issues = orm_insert_into_raw(new_raw_id, new_bulletin_id)
            new_raw_id = Raw.objects.get(id = new_raw_id)
            adress_line = x['street'] + ", "+ x['postal_code'] + " "+ x['city']
            out = json.dumps({
                                "id": new_id,
                                "br_court_name": x['br_court_name'],
                                "kind_name": x['kind_name'],
                                "cin": x['cin'],
                                "registration_date": x['registration_date'],
                                "corporate_body_name": x['corporate_body_name'],
                                "br_section": x['br_section'],
                                "br_insertion": x['br_insertion'],
                                "street": x['street'],
                                "postal_code": x['postal_code'],
                                "city": x['city'],
                                "address_line": adress_line
                                })
            out_final = json.loads(out)
            insert = orm_insert_into_podanie(out_final, new_bulletin_id, new_raw_id)
            response = JsonResponse(out_final, safe=False)
            response.status_code = 201
            return response


    elif request.method == 'GET':
        if request.GET.get('order_by') != None:
            order = str(request.GET.get('order_by'))
    
        else:
            order = "id"

        if request.GET.get('order_type') != None:
            order_type = str(request.GET.get('order_type'))
    
        else:
            order_type = "desc"


        if request.GET.get('per_page') != None:
            limit = int(request.GET.get('per_page'))
    
        else:
            limit = 10
    
        if request.GET.get('page') != None:
            page_num = int(request.GET.get('page'))
        else:
            page_num = 1

        if request.GET.get('query') != None:
            query = request.GET.get('query')
            query = query.split()
        else:
            query = "none"


        if request.GET.get('registration_date_gte') != None:
            reg_gte = request.GET.get('registration_date_gte')
        else:
            reg_gte = "none"
        
        if request.GET.get('registration_date_lte') != None:
            reg_lte = request.GET.get('registration_date_lte')
        else:
            reg_lte = "none"

    offset = limit * (int(page_num) - 1)
    limit = limit + offset

    result = get_orm_query(order, order_type, query, limit, offset, reg_gte, reg_lte)

    meta_limit = limit - offset

    total = orm_count(query, reg_gte, reg_lte)

    list_result = list(result)

    meta = {
            "page": int(page_num),
            "per_page": int(meta_limit),
            "pages": math.ceil(int(total)/limit),
            "total": int(total)
        }

    c = json.dumps({"items":list_result, "metadata": meta}, indent=4, sort_keys=True, default=str)
    x = json.loads(c)

    return JsonResponse(x, safe=False)


@csrf_exempt
def orm_podanie_modification(request, id):
    if request.method == 'DELETE':
        if Podanie.objects.filter(id = id).exists():            
            result = Podanie.objects.filter(id = id).delete()
            c = json.dumps({})
            x = json.loads(c)
            
            response = JsonResponse(x ,safe=False)
            response.status_code = 204

            return response
        else:
            c = json.dumps({})
            x = json.loads(c)
            response = JsonResponse(x ,safe=False)
            response.status_code = 404
            return response
    
    elif request.method == 'GET':
        if Podanie.objects.filter(id = id).exists():            
            result = Podanie.objects.filter(id = id).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")
            final_result = list(result)
            c = json.dumps({"items":final_result}, indent=4, sort_keys=True, default=str)
            x = json.loads(c)
            
            response = JsonResponse(x ,safe=False)
            response.status_code = 201
            

            return response
        else:
            c = json.dumps({})
            x = json.loads(c)
            response = JsonResponse(x ,safe=False)
            response.status_code = 404
            return response

    elif request.method == 'PUT':
        if Podanie.objects.filter(id = id).exists():
            body = request.body.decode('utf-8')
            x = json.loads(body)

            record = Podanie.objects.get(id = id)

            if 'br_court_name' in x:
                record.br_court_name = x['br_court_name']
        
            if 'kind_name' in x:
                record.kind_name = x['kind_name']
            if 'cin' in x and isinstance(x['cin'], int):
                record.cin = x['cin']
            if 'registration_date' in x:
                record.registration_date = x['registration_date']
            if 'corporate_body_name' in x:
                record.corporate_body_name = x['corporate_body_name']
            if 'br_section' in x:
                record.br_section = x['br_section']
            if 'br_insertion' in x:
                record.br_insertion = x['br_insertion']
            if 'street' in x:
                record.street = x['street']
            if 'postal_code' in x:
                record.postal_code = x['postal_code']
            if 'city' in x:
                record.city = x['city']
            
            record.save()

            result = Podanie.objects.filter(id = id).values("id", "br_court_name", "kind_name", "cin", "registration_date", "corporate_body_name", "br_section", "br_insertion", "text", "street", "postal_code", "city")
            final_result = list(result)
            c = json.dumps({"items":final_result}, indent=4, sort_keys=True, default=str)
            x = json.loads(c)
            
            response = JsonResponse(x ,safe=False)
            response.status_code = 201
            

            return response
        else:
            c = json.dumps({})
            x = json.loads(c)
            response = JsonResponse(x ,safe=False)
            response.status_code = 404
            return response


##########################################
###########companies view ################
##########################################
def orm_companies_count(query, gte, lte):
    
    if query == "none" and gte == "none" and lte == "none":
        result = Companies.objects.count()
    elif gte == "none" and lte == "none":
        result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query])).count()    
    elif gte == "none":
        result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__lte = lte).count()
    elif lte == "none":
        result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__gte = gte).count()
    elif query == "none" and gte == "none":
        result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                last_update__lte = lte).count()
    elif query == "none" and lte == "none":
       result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                last_update__gte = gte).count()
    elif query == "none":
        result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                last_update__gte = gte, last_update__lte = lte).count()
    else:
        result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line')).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__gte = gte, last_update__lte = lte).count()
    return result

def get_orm_companies_query(order, order_type, query, limit, offset, gte, lte):
    
    if query == "none" and gte == "none" and lte == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]

    elif gte == "none" and lte == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query])).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query])).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
                 
    elif gte == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__lte = lte).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__lte = lte).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
            
                
    elif lte == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__gte = gte).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__gte = gte).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]

            

    elif query == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(               
                last_update__lte = lte, last_update__gte = gte).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                last_update__lte = lte, last_update__gte = gte).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
            
    elif query == "none" and gte == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                last_update__lte = lte).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                last_update__lte = lte).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]

            
    elif query == "none" and lte == "none":
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                last_update__gte = gte).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                last_update__gte = gte).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
            
    else:
        if order_type == "desc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__gte = gte, last_update__lte = lte).order_by(F(order).desc(nulls_last=True)).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]
        elif order_type == "asc":
            result = Companies.objects.annotate(search=SearchVector('name') + SearchVector('address_line'), or_podanie_issues_count=Count('podanie', distinct=True), znizenie_imania_issues_count=Count('znizenieimaniaissues', distinct=True), likvidator_issues_count=Count('likvidatorissues', distinct=True), konkurz_vyrovnanie_issues_count=Count('konkurzvyrovnanieissues', distinct=True), konkurz_restrukturalizacia_actors_count=Count('konkurzrestrukturalizaciaactors', distinct=True)).filter(
                reduce(lambda x, y: x | y, [Q(search=item) for item in query]), last_update__gte = gte, last_update__lte = lte).order_by(order).values('cin', 'name', 'address_line', 'last_update', 'or_podanie_issues_count', 'znizenie_imania_issues_count', 'likvidator_issues_count', 'konkurz_vyrovnanie_issues_count', 'konkurz_restrukturalizacia_actors_count')[offset:limit]

            
    
    return result
@csrf_exempt
def orm_companies_view(request):


    if request.method == 'GET':

        if request.GET.get('order_by') != None:
            order = str(request.GET.get('order_by'))
    
        else:
            order = "cin"

        if request.GET.get('order_type') != None:
            order_type = str(request.GET.get('order_type'))
    
        else:
            order_type = "desc"


        if request.GET.get('per_page') != None:
            paginator_size = int(request.GET.get('per_page'))
    
        else:
            paginator_size = 1
    
        if request.GET.get('page') != None:
            page_num = int(request.GET.get('page'))
        else:
            page_num = 1

        if request.GET.get('query') != None:
            query = request.GET.get('query')
            query = query.split()
            
        else:
            query = "none"


        if request.GET.get('last_update_gte') != None:
            last_gte = request.GET.get('last_update_gte')
        else:
            last_gte = "none"
        
        if request.GET.get('last_update_lte') != None:
            last_lte = request.GET.get('last_update_lte')
        else:
            last_lte = "none"

        offset = paginator_size * (int(page_num) - 1)
        limit = paginator_size + offset
        
        total = orm_companies_count(query, last_gte, last_lte)

        table = get_orm_companies_query(order, order_type, query, limit, offset, last_gte, last_lte)

        table = list(table)

        
        meta = {
            "page": int(page_num),
            "per_page": int(paginator_size),
            "pages": math.ceil(int(total)/limit),
            "total": int(total)
        }
        
    
        c = json.dumps({"items": table, "metadata": meta}, indent=4, sort_keys=True, default=str)
        x = json.loads(c)
    
        return JsonResponse(x, safe=False)
