from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _



class Bulletin(models.Model):
    class Meta:
        db_table = 'ov.bulletin_issues'
        app_label = 'dbs'

    year = models.IntegerField()
    number = models.IntegerField()
    published_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Raw(models.Model):
    class Meta:
        db_table = 'ov.raw_issues'
        app_label = 'dbs'

    bulletin_issue = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class Podanie(models.Model):
    class Meta:
        db_table = 'ov.or_podanie_issues'
        app_label = 'dbs'

    br_section = models.CharField(max_length=250)
    br_insertion = models.CharField(max_length=250)
    br_mark = models.CharField(max_length=100)
    br_court_code = models.CharField(max_length=250)
    br_court_name = models.CharField(max_length=250)
    corporate_body_name = models.CharField(max_length=250)
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=250)
    kind_code = models.CharField(max_length=250)
    kind_name = models.CharField(max_length=250)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cin = models.BigIntegerField()
    registration_date = models.DateTimeField(auto_now=True)
    address_line = models.CharField(max_length=250)
    bulletin_issue =  models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    raw_issue = models.ForeignKey(Raw, on_delete=models.CASCADE)
    company = models.ForeignKey('Companies', models.DO_NOTHING, blank=True, null=True)
    

class Companies(models.Model):
    cin = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    br_section = models.CharField(max_length=150, blank=True, null=True)
    address_line = models.CharField(max_length=150)
    last_update = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ov.companies'



class KonkurzRestrukturalizaciaActors(models.Model):
    corporate_body_name = models.CharField(max_length=150, blank=True, null=True)
    cin = models.BigIntegerField(blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    building_number = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.ForeignKey('Companies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ov.konkurz_restrukturalizacia_actors'


class KonkurzRestrukturalizaciaIssues(models.Model):
    bulletin_issue = models.ForeignKey(Bulletin, models.DO_NOTHING)
    raw_issue = models.OneToOneField(Raw, models.DO_NOTHING)
    court_name = models.CharField(max_length=150)
    file_reference = models.CharField(max_length=150)
    ics = models.CharField(max_length=150)
    released_by = models.CharField(max_length=150)
    releaser_position = models.CharField(max_length=150, blank=True, null=True)
    sent_by = models.CharField(max_length=150, blank=True, null=True)
    released_date = models.DateField()
    debtor = models.ForeignKey(KonkurzRestrukturalizaciaActors, models.DO_NOTHING, blank=True, null=True)
    kind = models.CharField(max_length=150)
    heading = models.TextField(blank=True, null=True)
    decision = models.TextField(blank=True, null=True)
    announcement = models.TextField(blank=True, null=True)
    advice = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ov.konkurz_restrukturalizacia_issues'
        unique_together = (('updated_at', 'id'),)


class KonkurzRestrukturalizaciaProposings(models.Model):
    issue = models.ForeignKey(KonkurzRestrukturalizaciaIssues, models.DO_NOTHING)
    actor = models.ForeignKey(KonkurzRestrukturalizaciaActors, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ov.konkurz_restrukturalizacia_proposings'


class KonkurzVyrovnanieIssues(models.Model):
    bulletin_issue = models.ForeignKey(Bulletin, models.DO_NOTHING)
    raw_issue = models.OneToOneField(Raw, models.DO_NOTHING)
    court_code = models.CharField(max_length=150)
    court_name = models.CharField(max_length=150)
    file_reference = models.CharField(max_length=150)
    corporate_body_name = models.CharField(max_length=150)
    cin = models.BigIntegerField(blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    building_number = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    kind_code = models.CharField(max_length=150)
    kind_name = models.CharField(max_length=150)
    announcement = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.ForeignKey('Companies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ov.konkurz_vyrovnanie_issues'
        unique_together = (('updated_at', 'id'),)


class LikvidatorIssues(models.Model):
    bulletin_issue = models.ForeignKey(Bulletin, models.DO_NOTHING)
    raw_issue = models.OneToOneField(Raw, models.DO_NOTHING)
    legal_form_code = models.CharField(max_length=150)
    legal_form_name = models.CharField(max_length=150)
    corporate_body_name = models.CharField(max_length=150)
    cin = models.BigIntegerField()
    sid = models.CharField(max_length=150, blank=True, null=True)
    street = models.CharField(max_length=150)
    building_number = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    postal_code = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    in_business_register = models.BooleanField()
    br_insertion = models.CharField(max_length=150, blank=True, null=True)
    br_court_code = models.CharField(max_length=150, blank=True, null=True)
    br_court_name = models.CharField(max_length=150, blank=True, null=True)
    br_section = models.CharField(max_length=150, blank=True, null=True)
    other_registrar_name = models.CharField(max_length=150, blank=True, null=True)
    other_registration_number = models.CharField(max_length=150, blank=True, null=True)
    decision_based_on = models.CharField(max_length=150)
    decision_date = models.DateField()
    claim_term = models.CharField(max_length=150)
    liquidation_start_date = models.DateField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    debtee_legal_form_code = models.CharField(max_length=150, blank=True, null=True)
    debtee_legal_form_name = models.CharField(max_length=150, blank=True, null=True)
    company = models.ForeignKey('Companies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ov.likvidator_issues'
        unique_together = (('updated_at', 'id'),)


class OrPodanieIssueDocuments(models.Model):
    or_podanie_issue = models.ForeignKey(Podanie, models.DO_NOTHING)
    name = models.CharField(max_length=150)
    delivery_date = models.DateField()
    ruz_deposit_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ov.or_podanie_issue_documents'





class ZnizenieImaniaCeos(models.Model):
    znizenie_imania_issue = models.ForeignKey('ZnizenieImaniaIssues', models.DO_NOTHING)
    prefixes = models.CharField(max_length=150, blank=True, null=True)
    postfixes = models.CharField(max_length=150, blank=True, null=True)
    given_name = models.CharField(max_length=150, blank=True, null=True)
    family_name = models.CharField(max_length=150, blank=True, null=True)
    street = models.CharField(max_length=150, blank=True, null=True)
    building_number = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ov.znizenie_imania_ceos'


class ZnizenieImaniaIssues(models.Model):
    bulletin_issue = models.ForeignKey(Bulletin, models.DO_NOTHING)
    raw_issue = models.OneToOneField(Raw, models.DO_NOTHING)
    corporate_body_name = models.CharField(max_length=150)
    street = models.CharField(max_length=150, blank=True, null=True)
    building_number = models.CharField(max_length=150, blank=True, null=True)
    postal_code = models.CharField(max_length=150, blank=True, null=True)
    city = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=150, blank=True, null=True)
    br_court_code = models.CharField(max_length=150)
    br_court_name = models.CharField(max_length=150)
    br_section = models.CharField(max_length=150)
    br_insertion = models.CharField(max_length=150)
    cin = models.BigIntegerField()
    decision_text = models.TextField(blank=True, null=True)
    decision_date = models.DateField(blank=True, null=True)
    equity_currency_code = models.CharField(max_length=150)
    old_equity_value = models.DecimalField(max_digits=12, decimal_places=2)
    new_equity_value = models.DecimalField(max_digits=12, decimal_places=2)
    resolution_store_date = models.DateField(blank=True, null=True)
    first_ov_released_date = models.DateField(blank=True, null=True)
    first_ov_released_number = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    company = models.ForeignKey('Companies', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ov.znizenie_imania_issues'
        unique_together = (('updated_at', 'id'),)



