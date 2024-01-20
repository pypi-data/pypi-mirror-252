import json
import uuid
import threading
import io
import chardet
import re
import os
import pandas as pd

from django.db.models import Q
from django.core.paginator import Paginator
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from zippy_form.models import Account, FormField, Form, FormStep, FormSubmission, FormSubmissionData, FormFieldOption, Webhook,WebhookForm, AccountPaymentSettings,FormPaymentSettings, PaymentGatewayWebhook, FormSubmissionPaymentDetails
from zippy_form.serializers import FormSerializer, FormStepSerializer, MapFieldToFormStepSerializer, UpdateFieldSettingsSerializer, \
    ReOrderFieldSerializer, AccountSerializer, WebhookSerializer, FormPaymentSettingsSerializer, AccountProfileUpdateSerializer, AccountPaymentUpdateSerializer
from zippy_form.utils import FORM_STATUS, FORM_FIELD_STATUS, FIELD_TYPES, FORM_SUBMISSION_STATUS, \
    FORM_SUBMISSION_STATUS_DETAILS, FORM_STEP_STATUS, FIELD_RULES, FORM_FIELD_OPTION_STATUS, FIELD_RULES_FILE_FORMAT_ALLOWED, \
    FORM_STATUS_DETAILS, FORM_FIELD_DETAILS, FORM_STEP_STATUS_DETAILS, ACCOUNT_STATUS, ACCOUNT_STATUS_DETAILS, WEBHOOK_STATUS, \
    WEBHOOK_STATUS_DETAILS ,FORM_TYPE_DETAILS, FORM_TYPE, PAYMENT_MODE, PAYMENT_GATEWAYS,APPLICATION_TYPE,PAYMENT_TYPE, \
    DEFAULT_STRIPE_APPLICATION_FEE_AMOUNT, PAYMENT_TYPE_DETAILS, PAYMENT_MODE_DETAILS, convert_utc_to_timezone,get_stripe_secret_key,get_stripe_public_key,get_stripe_connect_url, \
    format_form_submission_status, generate_url_qrcode
from zippy_form.validation_rule import validate_is_empty, validate_minlength, validate_maxlength, validate_is_url,\
    validate_is_unique, validate_is_number, validate_min_value, validate_max_value, validate_is_email, validate_is_date,\
    validate_min_max_selection, validate_is_file, validate_file_extension, validate_file_size, validate_is_time
from zippy_form.event_webhook_triggers import after_account_create, after_form_create, after_form_submit
from zippy_form.gsheet import create_gsheet_map_form, send_form_data_to_gsheet, remove_form_data_from_gsheet, \
    add_field_labels_to_gsheet, update_field_label_in_gsheet, remove_field_from_gsheet
from zippy_form.permissions import IsAccountActive
from zippy_form.payments.stripe_payment import stripe_connect
from zippy_form.payments.__init__ import Payment

try:
    DEFAULT_PAGE_SIZE = settings.ZF_LIST_PER_PAGE
except:
    DEFAULT_PAGE_SIZE = 8

@api_view(['GET'])
def account_list(req):
    """
    Get list of active accounts
    """
    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    page_size = req.GET.get('page_size', DEFAULT_PAGE_SIZE)

    # Get only non deleted accounts
    accounts = Account.objects.exclude(status=ACCOUNT_STATUS[0][0]).order_by('-created_date')

    paginator = Paginator(accounts, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page"

        return Response({"status": "error", "msg": "Invalid Page", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each form
        for account in page_obj.object_list:
            active_form_count = Form.objects.filter(account=account).exclude(status=FORM_STATUS[0][0]).count()

            single_row_entry = {}
            single_row_entry['id'] = account.id
            single_row_entry['name'] = account.name
            single_row_entry['admin_email'] = account.admin_email
            single_row_entry['timezone'] = account.timezone
            single_row_entry['meta_detail'] = account.meta_detail
            single_row_entry['active_form_count'] = active_form_count
            single_row_entry['status'] = account.status
            single_row_entry['status_text'] = ACCOUNT_STATUS_DETAILS[account.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_account(req):
    """
    Create Account
    """
    serializer = AccountSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()
        response_data = {}
        response_data['id'] = instance.id

        # Event & Webhook - Account Create
        event_data = {"event": "account.created", "account": {"id": str(instance.id), "meta_detail": instance.meta_detail}}
        after_account_create(event_data)

        return Response({"status": "success", "data": response_data, "msg": "Account Created Successfully"},
                        status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_account_details(req, account_id):
    """
    Get Account Details
    """
    try:
        account = Account.objects.filter(id=account_id, status=ACCOUNT_STATUS[1][0]).get()
    except Account.DoesNotExist:
        return Response({"status":'error',"msg": "Invalid Account ID"}, status=status.HTTP_400_BAD_REQUEST)

    account_payment_settings_detail = {
        "name": account.name,
        "admin_email": account.admin_email,
        "is_payment_collect_enabled":account.is_payment_collect_enabled,
        "primary_payment_gateway":account.primary_payment_gateway,
        "meta_detail":account.meta_detail
    }

    return Response({"status": "success", "data": account_payment_settings_detail}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_account_payment_details(req,account_id):
    """
    Account Payment Details Update
    """
    try:
        account = Account.objects.filter(id=account_id, status=ACCOUNT_STATUS[1][0]).get()
    except Account.DoesNotExist:
        return Response({"status":'error',"msg": "Invalid Account ID"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = AccountPaymentUpdateSerializer(account, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()
        response_data = {}
        response_data['id'] = instance.id

        return Response({"status": "success", "data": response_data, "msg": "Payment Settings Updated Successfully"},
                        status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_account_profile_details(req,account_id):
    """
    Account User Details Update
    """
    try:
        account = Account.objects.filter(id=account_id, status=ACCOUNT_STATUS[1][0]).get()
    except Account.DoesNotExist:
        return Response({"status":'error',"msg": "Invalid Account ID"}, status=status.HTTP_400_BAD_REQUEST)

    if req.data.get('is_payment_collect_enabled') is not None and req.data.get(
            'is_payment_collect_enabled').lower() == 'true':
        serializer = AccountProfileUpdateSerializer(account, data=req.data)

        if not serializer.is_valid():
            return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance = serializer.save()
            response_data = {}
            response_data['id'] = instance.id
    else:
        account.is_payment_collect_enabled = False
        account.primary_payment_gateway = ''
        account.save()
        response_data = {}
        response_data['id'] = account.id

    return Response({"status": "success", "data": response_data, "msg": "Profile Details Updated Successfully"},
                        status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAccountActive])
def form_list(req):
    """
    Get list of non deleted forms mapped to the account
    """
    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    search_by_keyword = req.GET.get('search', None)
    filter_by_status = req.GET.get('status', None)
    filter_by_type = req.GET.get('type', None)
    page_size = req.GET.get('page_size', DEFAULT_PAGE_SIZE)
    exclude_categories = req.GET.getlist('exclude_categories', [])

    account_id = req.headers['ZF-SECRET-KEY']

    # Get only non deleted forms
    forms = Form.objects.filter(account_id=account_id).exclude(status=FORM_STATUS[0][0]).order_by('-created_date')

    if exclude_categories:
        forms = forms.exclude(category__in=exclude_categories)
    if search_by_keyword:
        forms = forms.filter(Q(name__icontains=search_by_keyword))
    if filter_by_status:
        forms = forms.filter(status=filter_by_status)
    if filter_by_type:
        forms = forms.filter(type=filter_by_type)

    paginator = Paginator(forms, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page"

        return Response({"status": "error", "msg": "Invalid Page", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each form
        for form in page_obj.object_list:
            # Get non deleted form submission count
            form_submission_count = FormSubmission.objects.filter(form_id=form.id).exclude(status=FORM_SUBMISSION_STATUS[0][0]).count()

            single_row_entry = {}
            single_row_entry['id'] = form.id
            single_row_entry['name'] = form.name
            single_row_entry['description'] = form.description
            single_row_entry['meta_detail'] = form.meta_detail
            single_row_entry['form_type'] = FORM_TYPE_DETAILS[form.type]
            single_row_entry['gsheet_url'] = form.gsheet_url
            single_row_entry['form_submission_count'] = form_submission_count
            single_row_entry['status'] = form.status
            single_row_entry['status_text'] = FORM_STATUS_DETAILS[form.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAccountActive])
def form_list_without_pagination(req):
    """
    Get list of non deleted forms mapped to the account without pagination
    """
    response_data = {'list': {}}

    account_id = req.headers['ZF-SECRET-KEY']

    exclude_categories = req.GET.getlist('exclude_categories', [])

    # Get only active forms
    forms = Form.objects.filter(account_id=account_id, status=FORM_STATUS[1][0])

    if exclude_categories:
        forms = forms.exclude(category__in=exclude_categories)

    forms = forms.order_by('-created_date')

    data = []
    # Loop each form
    for form in forms:

        single_row_entry = {}
        single_row_entry['id'] = form.id
        single_row_entry['name'] = form.name

        data.append(single_row_entry)
    response_data['list']['data'] = data

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAccountActive])
def create_form(req):
    """
    Create form with status draft with step 1 under an Account - To be used when clicking "Add Form" from the form builder
    """
    meta_detail = req.data.get("meta_detail", "")
    form_type = req.data.get('type', FORM_TYPE[0][0])

    account_id = req.headers['ZF-SECRET-KEY']

    try:
        account = Account.objects.filter(id=account_id, status=ACCOUNT_STATUS[1][0]).get()
    except Exception as e:
        return Response({"status": "error", "msg": "Invalid Account ID"},
                        status=status.HTTP_400_BAD_REQUEST)
    _is_valid_payment_type = True
    for form_type_obj in FORM_TYPE:
        if form_type_obj[0] == form_type:
            _is_valid_payment_type = False
            break
    if _is_valid_payment_type:
        return Response({"status": "error", "msg": "Invalid Form Type"},
                        status=status.HTTP_400_BAD_REQUEST)

    if form_type == FORM_TYPE[1][0]:
        # Handle for Payment Form
        is_payment_collect_enabled = account.is_payment_collect_enabled
        if not is_payment_collect_enabled:
            return Response({"status": "error", "msg": "Payment settings must be enabled in your account before creating a payment form.", "enable_settings_link": True},
                            status=status.HTTP_400_BAD_REQUEST)

    form = Form.objects.create(name="Untitled Form", account_id= account_id, meta_detail=meta_detail, type=form_type)

    form_step = FormStep.objects.create(
        name="Step 1",
        step_order=1,
        form=form,
    )

    # Create Gsheet & map to form - if form submission is allowed to sync on Gsheet
    gsheet = threading.Thread(target=create_gsheet_map_form, args=(form,))
    gsheet.start()

    # Create QR Code for Form
    custom_form_frontend_url = getattr(settings, 'ZF_CUSTOM_FORM_FRONTEND_URL', "")
    qr_code = generate_url_qrcode(form.id, custom_form_frontend_url + str(form.id))

    form.qrcode = os.path.relpath(qr_code, settings.MEDIA_ROOT)
    form.save()

    steps = []
    response_data = {'form': {}, 'steps': steps}

    response_data['form']['id'] = str(form.id)
    response_data['form']['name'] = form.name
    response_data['form']['description'] = ''
    response_data['form']['class_name'] = ''
    response_data['form']['type'] = form.type
    response_data['form']['meta_detail'] = form.meta_detail
    response_data['form']['success_msg'] = ''
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    step_details = {'id': form_step.id, 'name': form_step.name, 'description': '', 'is_current_step': True}
    steps.append(step_details)

    # Event & Webhook - Form Create
    event_data = {
        "event": "form.created",
        "account": {"id": str(form.account.id), "meta_detail": form.account.meta_detail},
        "form": response_data['form']
    }
    after_form_create(event_data)

    return Response({"status": "success", "data": response_data, "msg": "Form Created Successfully"},
                    status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def update_form_name(req, form_id):
    """
    Update form name
    * Update form name
    """
    try:
        # Update only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    serializer = FormSerializer(form, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        old_form_name = form.name
        new_form_name = serializer.validated_data['name']

        serializer.save()

    # Update Product In Payment Gateway if Form Status is Active
    if form.status == FORM_STATUS[1][0]:
        if old_form_name != new_form_name:
            # Update Product Name Only if the form name changed
            account = form.account
            is_payment_collect_enabled = account.is_payment_collect_enabled

            if is_payment_collect_enabled:
                # If Tenant Account enabled Payment Collection

                # Get Tenant Account Primary Payment Gateway
                primary_payment_gateway = account.primary_payment_gateway

                payment_setting = FormPaymentSettings.objects.filter(form_id=form_id, payment_gateway=primary_payment_gateway).first()

                if payment_setting is not None:
                    # Get form payment mode(test, live)
                    form_payment_method = payment_setting.payment_mode

                    application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])

                    if primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
                        # Handle for stripe
                        secret_key = get_stripe_secret_key(form.primary_payment_mode)
                        product_id = payment_setting.stripe_product_id

                    # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

                    if application_type == APPLICATION_TYPE[1][0]:
                        # If the application configured as "saas" application
                        account_payment_settings = account.account_payment_settings.filter(
                            payment_gateway=primary_payment_gateway, payment_mode=form_payment_method).first()
                        if account_payment_settings and account_payment_settings.key:
                            connected_account_id = account_payment_settings.key

                            if  secret_key and connected_account_id and product_id:
                                payment = Payment(primary_payment_gateway, secret_key, APPLICATION_TYPE[1][0], connected_account_id)
                                payment.update_product(product_id, form.name)
    # Update Product In Payment Gateway if Form Status is Active

    response_data = {'form': {}}
    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['description'] = ''
    response_data['form']['class_name'] = ''
    response_data['form']['success_msg'] = ''
    response_data['form']['meta_detail'] = form.meta_detail
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    return Response({"status": "success", "data": response_data, "msg": "Form Name Updated Successfully"},
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def get_form_gsheet_url(req, form_id):
    """
    Get Form GSheet URL
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except ObjectDoesNotExist:
        return Response({"status": "error", "data": "Form Does not Exits"}, status=status.HTTP_400_BAD_REQUEST)

    gsheet_url = form.gsheet_url
    return Response({"status": "success", "data": gsheet_url},status=status.HTTP_200_OK)




@api_view(['PUT'])
def update_form(req, form_id):
    """
    Update form
    * Update form & field status from Draft to Active
    """
    try:
        # Update only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    step_id = req.data.get('step_id')

    error = {}
    if not step_id:
        error['step_id']=['This field is required']
    else:
        step = FormStep.objects.filter(id=step_id, form=form_id).first()
        if not step:
            error['step_id']=['Invalid Form Step ID']

    if error !={}:
        return Response({'status':'validation_error', 'data':error}, status=status.HTTP_400_BAD_REQUEST)

    # Update draft form to active status
    if form.status == FORM_STATUS[3][0]:
        form.status = FORM_STATUS[1][0]
        form.save()

    _draft_fields = []

    # Update draft fields of the form to active status, which has field settings updated
    form_fields = form.form_fields.filter(status=FORM_FIELD_STATUS[3][0]).filter(is_field_settings_updated=True).order_by('field_order')
    fields_to_exclude = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]
    for form_field in form_fields:
        temp = {}
        temp['id'] = str(form_field.id)
        temp['label'] = form_field.label

        if form_field.field_type not in fields_to_exclude:
            _draft_fields.append(temp)

        form_field.status = FORM_FIELD_STATUS[1][0]
        form_field.save()

    # Get all active fields of the step
    active_fields = form.form_fields.filter(form_step=step_id, status=FORM_FIELD_STATUS[1][0]).filter(is_field_settings_updated=True).order_by('field_order').values_list('id', flat=True)

    # Add new field label to gsheet(When field status update from "draft" to "active, sync to gsheet)
    gsheet = threading.Thread(target=add_field_labels_to_gsheet, args=(_draft_fields, form))
    gsheet.start()

    response_data = {'form': {}}

    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['description'] = ''
    response_data['form']['class_name'] = ''
    response_data['form']['success_msg'] = ''
    response_data['form']['meta_detail'] = form.meta_detail
    response_data['form']['active_fields'] = active_fields
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    return Response({"status": "success", "data": response_data, "msg": "Form Updated Successfully"},
                    status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_form_status(req, form_id):
    """
    Update form status
    * Active to InActive
    * InActive to Active
    """
    try:
        # Update form status only for the non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    if form.status == FORM_STATUS[1][0]:
        # Update form status from Active to InActive
        form.status = FORM_STATUS[2][0]
        form.save()
    elif form.status == FORM_STATUS[2][0]:
        # Update form status from InActive to Active
        form.status = FORM_STATUS[1][0]
        form.save()

    response_data = {'form': {}}

    response_data['form']['id'] = form.id

    return Response({"status": "success", "data": response_data, "msg": "Form Status Updated Successfully"},
                    status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_form(req, form_id):
    """
    Soft delete form
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    # Soft delete form
    form.status = FORM_STATUS[0][0]
    form.save()

    response_data = {'form': {}}

    response_data['form']['id'] = form.id

    return Response({"status": "success", "data": response_data, "msg": "Form Deleted Successfully"},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def form_submission_list(req, form_id):
    """
    Get list of form submissions
    """
    account_id = req.headers.get('ZF-SECRET-KEY')

    if account_id is None:
        data = "Secret Key Required"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)
    if account_id == '':
        data = "Secret Key Missing"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Get submission only for the non deleted form
        form = Form.objects.filter(id=form_id, account=account_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form or Account ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    page_size = req.GET.get('page_size', DEFAULT_PAGE_SIZE)
    filter_by_status = req.GET.get('status', '')

    allowed_status_filter = ['active', 'draft', 'payment_pending']
    if filter_by_status not in allowed_status_filter:
        filter_by_status = ''

    form_type = form.type
    form_name = form.name
    gsheet_url = form.gsheet_url
    account_timezone = form.account.timezone
    total_amount = 0

    # Get only non deleted form submission & based on filter
    form_submissions = FormSubmission.objects.filter(form=form_id)
    if filter_by_status:
        form_submissions = form_submissions.filter(status=filter_by_status)
    form_submissions = form_submissions.exclude(status=FORM_SUBMISSION_STATUS[0][0]).order_by('-modified_date')

    paginator = Paginator(form_submissions, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page"

        return Response({"status": "error", "msg": "Invalid Page", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        column_headers = []
        column_field_id = []

        column_headers.append({"field_type": '_id', "label": 'Id', 'field_id': "_id"})
        column_headers.append({"field_type": '_status_id', "label": 'Status ID', "field_id": '_status_id'})
        column_headers.append({"field_type": '_status', "label": 'Status', "field_id": '_status'})
        column_headers.append({"field_type": '_updated_at', "label": 'Updated At', "field_id": '_updated_at'})

        if form_type == FORM_TYPE[1][0]:
            column_headers.append({"field_type": '_payment_mode', "label": 'Payment Mode', "field_id": '_payment_mode'})
            column_headers.append({"field_type": '_total_amount_paid', "label": 'Total Amount Paid', "field_id": '_total_amount_paid'})

        # Get only active fields which are configured to show on table
        table_form_fields = form.form_fields.filter(status=FORM_FIELD_STATUS[1][0]).filter(show_on_table=True) \
            .order_by('table_field_order')

        # From above queryset - Get the "Column Headers" & "Field ID"
        for table_form_field in table_form_fields:
            column_headers.append({"field_type": table_form_field.field_type, "label": table_form_field.label, "field_id": str(table_form_field.id)})
            column_field_id.append(str(table_form_field.id))

        # column_headers.append({"field_type": '_status_id', "label": 'Status ID'})
        # column_headers.append({"field_type": '_status', "label": 'Status'})

        data = []
        # Loop each form submission
        for form_submission in page_obj.object_list:
            single_row_entry = []

            # default - "ID","Status ID","Status" at zero, first, second index for each submission
            single_row_entry.append(form_submission.id)
            single_row_entry.append(form_submission.status)
            single_row_entry.append(format_form_submission_status(form_submission.status, form_type))
            single_row_entry.append(convert_utc_to_timezone(str(form_submission.modified_date),
                                                                       account_timezone).strftime("%m-%d-%Y %H:%M:%S"))

            if form_type == FORM_TYPE[1][0]:
                form_submission_detail = FormSubmissionPaymentDetails.objects.filter(
                    form_submission=form_submission).order_by("-created_date").first()
                if form_submission_detail:
                    payment_mode = ""
                    total_amount = form_submission_detail.total
                else:
                    payment_mode = ""
                    total_amount = ""

                single_row_entry.append(payment_mode)
                single_row_entry.append(total_amount)

            # get the submitted data from "FormSubmissionData" - based on the "form submission" & the active fields
            # which are configured to show on table | getting all the values here, to reduce db call
            dynamic_field_values = FormSubmissionData.objects.filter(form_submission=form_submission) \
                .filter(form_field_id__in=column_field_id)

            formatted_dynamic_field_values = {}
            for dynamic_field_value in dynamic_field_values:
                field_type = dynamic_field_value.form_field.field_type
                if field_type == FIELD_TYPES[5][0]:
                    _values = format_string_to_json_array(dynamic_field_value.dropdown_field)
                    _option_values = get_field_option_values(_values)
                    if _values is not None:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
                    else:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
                elif field_type == FIELD_TYPES[6][0]:
                    _value = dynamic_field_value.radio_field
                    _option_value = get_field_option_value(_value)
                    formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_value
                # elif field_type == FIELD_TYPES[7][0]:
                #     formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.checkbox_field
                elif field_type == FIELD_TYPES[10][0]:
                    _value = dynamic_field_value.file_field
                    if _value:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _value.url
                    else:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = ""
                elif field_type == FIELD_TYPES[12][0]:
                    _values = format_string_to_json_array(dynamic_field_value.multiselect_checkbox_field)
                    if _values is not None:
                        _option_values = get_field_option_values(_values)
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
                    else:
                        formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
                else:
                    formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.text_field

            # loop the active fields which are configured to show on table & get the values added on the submission
            # using "formatted_dynamic_field_values"
            for column_field in column_field_id:
                if formatted_dynamic_field_values.get(column_field):
                    single_row_entry.append(formatted_dynamic_field_values.get(column_field))
                elif formatted_dynamic_field_values.get(column_field) == []:
                    single_row_entry.append([])
                else:
                    single_row_entry.append("")

            # default - "Status ID & Status" at last index for each submission
            # single_row_entry.append(form_submission.status)
            # single_row_entry.append(FORM_SUBMISSION_STATUS_DETAILS[form_submission.status])

            data.append(single_row_entry)

        response_data['form_type'] = form_type
        response_data['form_name'] = form_name
        response_data['gsheet_url'] = gsheet_url
        response_data['account_timezone'] = account_timezone
        response_data['column_headers'] = column_headers
        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def form_submission_details(req,form_id, form_submission_id):
    """
    Get form submission details
    """
    try:
        # Get only non deleted form submission
        form_submission = FormSubmission.objects.filter(id=form_submission_id).exclude(status=FORM_SUBMISSION_STATUS[0][0]).get()
    except FormSubmission.DoesNotExist:
        data = "Invalid Form Submission ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    form_submission_payment_detail = None

    form = form_submission.form
    if form:
        form_type = form.type
        form_name = form.name

        if form_type == FORM_TYPE[1][0]:
            # Get last Form Submission Payment Details
            form_submission_payment_detail = FormSubmissionPaymentDetails.objects.filter(
                form_submission=form_submission_id).order_by('-created_date').first()
    else:
        data = "Form Id Missing"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    column_headers = []
    column_field_id = []

    column_headers.append({"field_type": '_id', "label": 'Id'})

    # Get only active fields which are configured to show on table
    table_form_fields = form_submission.form.form_fields.filter(status=FORM_FIELD_STATUS[1][0]).order_by('table_field_order')

    # From above queryset - Get the "Column Headers" & "Field ID"
    for table_form_field in table_form_fields:
        column_headers.append({"field_type": table_form_field.field_type, "label": table_form_field.label})
        column_field_id.append(str(table_form_field.id))

    column_headers.append({"field_type": '_status', "label": 'Status'})
    column_headers.append({"field_type": '_status_id', "label": 'Status ID'})

    if form_type == FORM_TYPE[1][0]:
        if form_submission_payment_detail:
            column_headers.append({"field_type": '_payment_type', "label": 'Payment Type'})
            column_headers.append({"field_type": '_payment_mode', "label": 'Payment Mode'})
            column_headers.append({"field_type": '_currency', "label": 'Currency'})

            if form_submission_payment_detail.sub_total:
                column_headers.append({"field_type": '_price', "label": 'Price'})

            column_headers.append({"field_type": '_tax_percentage', "label": 'Tax Percentage'})
            column_headers.append({"field_type": '_tax_amount', "label": 'Tax Amount'})
            column_headers.append({"field_type": '_total_amount_paid', "label": 'Total Amount Paid'})


    single_row_entry = []

    # default - "ID" at first index for each submission
    single_row_entry.append(form_submission.id)

    # get the submitted data from "FormSubmissionData" - based on the "form submission" & the active fields
    # which are configured to show on table | getting all the values here, to reduce db call
    dynamic_field_values = FormSubmissionData.objects.filter(form_submission=form_submission) \
        .filter(form_field_id__in=column_field_id)

    formatted_dynamic_field_values = {}
    for dynamic_field_value in dynamic_field_values:
        field_type = dynamic_field_value.form_field.field_type
        if field_type == FIELD_TYPES[5][0]:
            _values = format_string_to_json_array(dynamic_field_value.dropdown_field)
            _option_values = get_field_option_values(_values)
            if _value is not None:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
            else:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
        elif field_type == FIELD_TYPES[6][0]:
            _value = dynamic_field_value.radio_field
            _option_value = get_field_option_value(_value)
            formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_value
        # elif field_type == FIELD_TYPES[7][0]:
        #     formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.checkbox_field
        elif field_type == FIELD_TYPES[10][0]:
            _value = dynamic_field_value.file_field
            if _value:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _value.url
            else:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = ""
        elif field_type == FIELD_TYPES[12][0]:
            _values = format_string_to_json_array(dynamic_field_value.multiselect_checkbox_field)
            if _values is not None:
                _option_values = get_field_option_values(_values)
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = _option_values
            else:
                formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = []
        else:
            formatted_dynamic_field_values[str(dynamic_field_value.form_field.id)] = dynamic_field_value.text_field

    # loop the active fields which are configured to show on table & get the values added on the submission
    # using "formatted_dynamic_field_values"
    for column_field in column_field_id:
        if formatted_dynamic_field_values.get(column_field):
            single_row_entry.append(formatted_dynamic_field_values.get(column_field))
        elif formatted_dynamic_field_values.get(column_field) == []:
            single_row_entry.append([])
        else:
            single_row_entry.append("")

    # default - "Status & Status ID" at last index for each submission
    single_row_entry.append(format_form_submission_status(form_submission.status, form_type))
    single_row_entry.append(form_submission.status)

    if form_type == FORM_TYPE[1][0]:
        # Add details related to Payment, if the form is Payment Form
        if form_submission_payment_detail:
            payment_type = form_submission_payment_detail.payment_type
            if payment_type:
                payment_type = PAYMENT_TYPE_DETAILS[payment_type]

            payment_mode = form_submission_payment_detail.payment_mode
            if payment_mode:
                payment_mode = PAYMENT_MODE_DETAILS[payment_mode]

            currency = form_submission_payment_detail.currency
            price = form_submission_payment_detail.sub_total
            tax_percentage = form_submission_payment_detail.tax_percentage
            tax_amount = form_submission_payment_detail.tax_amount
            total_price_paid = form_submission_payment_detail.total

            single_row_entry.append(payment_type)
            single_row_entry.append(payment_mode)
            single_row_entry.append(currency)

            if payment_type == PAYMENT_TYPE[0][0]:
                single_row_entry.append(price)

            single_row_entry.append(tax_percentage + "%")
            single_row_entry.append(tax_amount)
            single_row_entry.append(total_price_paid)


    response_data = {}
    response_data['form_name'] = form_name
    response_data['data'] = single_row_entry
    response_data['column_headers'] = column_headers

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def form_submission_details2(req, form_id, form_submission_id):
    """
    Get form submission details
    """
    try:
        # Get only non-deleted form submission
        form_submission = FormSubmission.objects.filter(id=form_submission_id).exclude(
            status=FORM_SUBMISSION_STATUS[0][0]).get()
    except FormSubmission.DoesNotExist:
        data = "Invalid Form Submission ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    form_submission_payment_detail = None

    form = form_submission.form
    if form:
        form_type = form.type
        form_name = form.name

        if form_type == FORM_TYPE[1][0]:
            form_submission_payment_detail = FormSubmissionPaymentDetails.objects.filter(form_submission=form_submission_id).order_by('-created_date').first()

    else:
        data = "Form Id Missing"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    column_headers = []
    column_field_id = []

    column_headers.append({"field_type": '_id', "label": 'Id'})

    # Get only active fields which are configured to show on the table
    table_form_fields = form_submission.form.form_fields.filter(
        status=FORM_FIELD_STATUS[1][0]).order_by('table_field_order')

    # From the above queryset - Get the "Column Headers" & "Field ID"
    for table_form_field in table_form_fields:
        column_headers.append({"field_type": table_form_field.field_type, "label": table_form_field.label})
        column_field_id.append(str(table_form_field.id))

    column_headers.append({"field_type": '_status', "label": 'Status'})
    column_headers.append({"field_type": '_status_id', "label": 'Status ID'})

    single_row_entry = []

    # default - "ID" at the first index for each submission
    single_row_entry.append({"key": "ID", "value": form_submission.id})

    # get the submitted data from "FormSubmissionData" - based on the "form submission" & the active fields
    # which are configured to show on the table | getting all the values here, to reduce db call
    dynamic_field_values = FormSubmissionData.objects.filter(form_submission=form_submission) \
        .filter(form_field_id__in=column_field_id)

    formatted_dynamic_field_values = {}
    for dynamic_field_value in dynamic_field_values:
        field_type = dynamic_field_value.form_field.field_type
        key = dynamic_field_value.form_field.label  # Adjust key formatting
        if field_type == FIELD_TYPES[5][0]:
            _values = format_string_to_json_array(dynamic_field_value.dropdown_field)
            _option_values = get_field_option_values(_values)
            if _values is not None:
                formatted_dynamic_field_values[key] = _option_values
            else:
                formatted_dynamic_field_values[key] = []
        elif field_type == FIELD_TYPES[6][0]:
            _value = dynamic_field_value.radio_field
            _option_value = get_field_option_value(_value)
            formatted_dynamic_field_values[key] = _option_value
        # elif field_type == FIELD_TYPES[7][0]:
        #     formatted_dynamic_field_values[key] = dynamic_field_value.checkbox_field
        elif field_type == FIELD_TYPES[10][0]:
            _value = dynamic_field_value.file_field
            if _value:
                formatted_dynamic_field_values[key] = _value.url
            else:
                formatted_dynamic_field_values[key] = ""
        elif field_type == FIELD_TYPES[12][0]:
            _values = format_string_to_json_array(dynamic_field_value.multiselect_checkbox_field)
            if _values is not None:
                _option_values = get_field_option_values(_values)
                formatted_dynamic_field_values[key] = _option_values
            else:
                formatted_dynamic_field_values[key] = []
        else:
            formatted_dynamic_field_values[key] = dynamic_field_value.text_field

    # loop the active fields which are configured to show on the table & get the values added on the submission
    # using "formatted_dynamic_field_values"
    for i, column_field in enumerate(column_field_id):
        key = column_headers[i + 1]["label"]  # Adjust index and key formatting
        if formatted_dynamic_field_values.get(key):
            single_row_entry.append({"key": key, "value": formatted_dynamic_field_values.get(key)})
        elif formatted_dynamic_field_values.get(key) == []:
            single_row_entry.append({"key": key, "value": []})
        else:
            single_row_entry.append({"key": key, "value": ""})

    if form_submission_payment_detail:
        payment_type = form_submission_payment_detail.payment_type
        if payment_type:
            payment_type = PAYMENT_TYPE_DETAILS[payment_type]

        payment_mode = form_submission_payment_detail.payment_mode
        if payment_mode:
            payment_mode = PAYMENT_MODE_DETAILS[payment_mode]

        currency = form_submission_payment_detail.currency
        price = form_submission_payment_detail.sub_total
        tax_percentage = form_submission_payment_detail.tax_percentage
        tax_amount = form_submission_payment_detail.tax_amount
        total_price_paid = form_submission_payment_detail.total

        single_row_entry.append({"key": 'Payment Type', "value": payment_type})
        single_row_entry.append({"key": 'Payment Mode', "value": payment_mode})
        single_row_entry.append({"key": 'Currency', "value": currency})

        if payment_type == PAYMENT_TYPE[0][0]:
            single_row_entry.append({"key": 'Price', "value": price})

        single_row_entry.append({"key": 'Tax Percentage', "value": tax_percentage + "%"} )
        single_row_entry.append({"key": 'Tax Amount', "value": tax_amount})
        single_row_entry.append({"key": 'Total Amount Paid', "value": total_price_paid})

    account_timezone = form.account.timezone
    single_row_entry.append({"key": "Updated At", "value": convert_utc_to_timezone(str(form_submission.modified_date),
                                                                                  account_timezone).strftime("%m-%d-%Y %H:%M:%S")})

    # default - "Status & Status ID" at the last index for each submission
    single_row_entry.append({"key": "Status", "value": format_form_submission_status(form_submission.status, form_type)})
    single_row_entry.append({"key": "Status ID", "value": form_submission.status})

    return Response({"status": "success", 'form_name':form_name, "data": single_row_entry}, status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_form_submission(req,form_id, form_submission_id):
    """
    Delete Form Submission
    """
    try:
        # Get only non deleted form submission
        form_submission = FormSubmission.objects.filter(id=form_submission_id).exclude(status=FORM_SUBMISSION_STATUS[0][0]).get()
    except FormSubmission.DoesNotExist:
        data = "Invalid Form Submission ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    form = form_submission.form

    form_submission.status = FORM_SUBMISSION_STATUS[0][0]
    form_submission.save()

    # Remove Form Data From Gsheet
    gsheet = threading.Thread(target=remove_form_data_from_gsheet, args=(form, str(form_submission_id)))
    gsheet.start()

    return Response({"status": "success", "msg": "Form Submission Deleted Successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def steps_mapped_to_form(req, form_id):
    """
    Get steps mapped to form
    """
    try:
        # Get form steps only for the non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    page_size = req.GET.get('page_size', DEFAULT_PAGE_SIZE)

    form_steps = form.form_steps.exclude(status=FORM_STEP_STATUS[0][0]).order_by('step_order')

    paginator = Paginator(form_steps, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page"

        return Response({"status": "error", "msg": "Invalid Page", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each step
        for form_step in page_obj.object_list:
            single_row_entry = {}
            single_row_entry['id'] = form_step.id
            single_row_entry['name'] = form_step.name
            single_row_entry['description'] = form_step.description
            single_row_entry['status'] = form_step.status
            single_row_entry['status_text'] = FORM_STEP_STATUS_DETAILS[form_step.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_form_step(req):
    """
    Create form step & map to form
    """
    serializer = FormStepSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()

        response_data = {'step': {}}

        response_data['step']['id'] = instance.id
        response_data['step']['name'] = instance.name

        return Response({"status": "success", "data": response_data, "msg": "Form Step Created Successfully"},
                        status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def update_form_step(req, step_id):
    """
    Update form step
    """
    try:
        form_step = FormStep.objects.filter(id=step_id).exclude(status=FORM_STATUS[0][0]).get()
    except FormStep.DoesNotExist:
        data = "Invalid Form Step ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    serializer = FormStepSerializer(form_step, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()

        response_data = {'step': {}}

        response_data['step']['id'] = instance.id
        response_data['step']['name'] = instance.name

        return Response({"status": "success", "data": response_data, "msg": "Form Step Updated Successfully"},
                        status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_form_step(req, step_id):
    """
    Soft delete form step
    """
    try:
        form_step = FormStep.objects.filter(id=step_id).exclude(status=FORM_STATUS[0][0]).get()
    except FormStep.DoesNotExist:
        data = "Invalid Form Step ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    #  Soft delete form step
    form_step.status = FORM_STEP_STATUS[0][0]
    form_step.save()

    response_data = {'step': {}}

    response_data['step']['id'] = form_step.id
    response_data['step']['name'] = form_step.name

    return Response({"status": "success", "data": response_data, "msg": "Form Step Deleted Successfully"},
                    status=status.HTTP_200_OK)


@api_view(['GET'])
def fields_mapped_to_form_step(req, form_id, step_id = None):
    """
    Get list of fields mapped to form step
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    # Get all step mapped to form - Query not executed here
    form_steps = form.form_steps.filter(status=FORM_STEP_STATUS[1][0]).order_by('step_order')

    if step_id is None:
        # Query executed here
        first_form_step = form_steps.first()
        if not first_form_step:
            data = "No Form Step Available"
            return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)
        current_step = str(first_form_step.id)
    else:
        # Check if the "step id" received from request is valid
        try:
            form.form_steps.filter(id=step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        except FormStep.DoesNotExist:
            data = "Invalid Form Step ID"
            return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

        current_step = step_id

    # Get only active fields
    form_fields = FormField.objects.filter(form_id=form_id).filter(form_step=current_step) \
        .exclude(status=FORM_FIELD_STATUS[0][0]).order_by('field_order').prefetch_related('form_field_options')

    steps = []
    fields = []

    custom_form_frontend_url = getattr(settings, 'ZF_CUSTOM_FORM_FRONTEND_URL', "")

    response_data = {'action': "#", 'form': {}, 'steps': steps, 'fields': fields}

    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['description'] = form.description
    response_data['form']['class_name'] = form.class_name
    response_data['form']['success_msg'] = form.success_msg
    response_data['form']['gsheet_url'] = form.gsheet_url
    response_data['form']['custom_form_url'] = custom_form_frontend_url + str(form.id)
    response_data['form']['qrcode_url'] = form.qrcode.url if form.qrcode else ""
    response_data['form']['type'] = form.type
    response_data['form']['admin_email'] = form.account.admin_email
    response_data['form']['status'] = form.status
    response_data['form']['status_text'] = FORM_STATUS_DETAILS[form.status]

    for form_step in form_steps:
        step = {}
        step['id'] = form_step.id
        step['name'] = form_step.name
        step['description'] = form_step.description

        if str(current_step) == str(form_step.id):
            step['is_current_step'] = True
        else:
            step['is_current_step'] = False

        steps.append(step)

    fields_to_exclude = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]

    for form_field in form_fields:
        if form_field.field_type in fields_to_exclude:
            label= ''
        else:
            label = form_field.label

        field_details = {
            'field_id': form_field.id,
            'field_type': form_field.field_type,
            'field_order': form_field.field_order,
            'field_size': form_field.field_size,
            'label': label,
            'slug': form_field.slug,
            'class_name': form_field.custom_class_name,
            'is_mandatory': form_field.is_mandatory,
        }

        field_type = form_field.field_type

        if field_type != FIELD_TYPES[14][0] and field_type != FIELD_TYPES[15][0]:
            field_details['placeholder'] = form_field.placeholder
            field_details['validations'] = form_field.validation_rule

        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            # Get Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
            field_options = []

            form_field_options = form_field.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0]).order_by(
                'option_order').all()
            for form_field_option in form_field_options:
                field_option = {
                    'value': form_field_option.id,
                    'label': form_field_option.label,
                }
                field_options.append(field_option)

            field_details['options'] = field_options

        if field_type == FIELD_TYPES[0][0] or field_type == FIELD_TYPES[1][0] or field_type == FIELD_TYPES[3][0] or \
                field_type == FIELD_TYPES[4][0] or field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[16][0]:
            # Text Box, Number, Email, Website URL, Dropdown
            field_details['field_format'] = form_field.field_format

        if field_type == FIELD_TYPES[14][0] or field_type == FIELD_TYPES[15][0]:
            # Heading, Paragraph
            field_details['content'] = form_field.content
            field_details['content_size'] = form_field.content_size
            field_details['content_alignment'] = form_field.content_alignment

        field_details['status'] = form_field.status
        field_details['status_text'] = FORM_FIELD_DETAILS[form_field.status]

        fields.append(field_details)

    response_data['fields'] = fields

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def map_field_to_form_step(req):
    """
    Map Field to Form Step with draft status
    """
    serializer = MapFieldToFormStepSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        try:
            # Map fields only for the non deleted form
            form = serializer.validated_data['form']
            form_id = form.id
            form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
        except Form.DoesNotExist:
            data = {}
            msg = []
            data['form'] = msg
            msg.append("Invalid Form ID")
            return Response({"status": "validation_error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Map fields only for the active step
            form_step = serializer.validated_data['form_step']
            form_step_id = form_step.id
            form_step = form.form_steps.filter(id=form_step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        except FormStep.DoesNotExist:
            data = {}
            msg = []
            data['form_step'] = msg
            msg.append("Invalid Form Step ID")
            return Response({"status": "validation_error", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        # Map field to form step
        field_order = serializer.validated_data['field_order']
        instance = serializer.save(table_field_order=field_order)

        response_data = {'field': {}}

        response_data['field']['id'] = instance.id
        response_data['field']['label'] = instance.label
        response_data['field']['type'] = instance.field_type

        return Response({"status": "success", "data": response_data, "msg": "Field Mapped To Form Successfully"},
                        status=status.HTTP_200_OK)


@api_view(['PUT'])
def re_order_field(req, form_id, step_id, field_id):
    """
    ReOrder Form Field
    """
    try:
        # ReOrder field only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ReOrder field only for non deleted field step
        form_steps = form.form_steps.filter(id=step_id).exclude(status=FORM_STEP_STATUS[0][0]).get()
    except FormStep.DoesNotExist:
        msg = "Invalid Form Step ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # ReOrder field only for non deleted field
        field = form_steps.form_step_fields.filter(id=field_id).exclude(status=FORM_FIELD_STATUS[0][0]).get()
    except FormField.DoesNotExist:
        msg = "Invalid Form Field ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ReOrderFieldSerializer(field, data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        new_field_order = int(req.POST.get('field_order'))
        old_field_order = field.field_order

        if old_field_order < new_field_order:
            # Moving field down, update fields between old and new position
            fields_to_update = FormField.objects.filter(form_step__id=step_id).filter(field_order__gt=old_field_order,
                                                        field_order__lte=new_field_order).order_by('field_order')
            for field in fields_to_update:
                field.field_order -= 1
                field.save()
        elif old_field_order > new_field_order:
            # Moving field up, update fields between new and old position
            fields_to_update = FormField.objects.filter(form_step__id=step_id).filter(field_order__gte=new_field_order,
                                                        field_order__lt=old_field_order).order_by('-field_order')
            for field in fields_to_update:
                field.field_order += 1
                field.save()

        instance = serializer.save()

        response_data = {'field': {}}

        response_data['field']['id'] = instance.id

        return Response({"status": "success", "data": response_data, "msg": "Field ReOrdered Successfully"},
                        status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_field_settings(req, form_id, field_id):
    """
    Update Field Settings
    """
    try:
        # Update field settings only for non deleted form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Update field settings only for non deleted field
        field = FormField.objects.filter(id=field_id).filter(form_id=form_id).exclude(status=FORM_FIELD_STATUS[0][0]).get()
        old_field_label = field.label
    except FormField.DoesNotExist:
        msg = "Invalid Form Field ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    serializer = UpdateFieldSettingsSerializer(field, data=req.data, context={'field_id': field_id, 'form_id': form_id})

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save(is_field_settings_updated=True)

        field_type = field.field_type
        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            # Save Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
            options = serializer.validated_data.get('options', [])
            create_update_field_options(options, field)

        response_data = {}

        field_details = {
            'field_id': instance.id,
            'field_type': field.field_type,
            'field_order': field.field_order,
            'field_size': instance.field_size,
            'class_name': instance.custom_class_name,
            'is_mandatory': instance.is_mandatory
        }
        field_type = field.field_type

        fields_to_exclude_label = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]

        if field_type in fields_to_exclude_label:
            label= ''
        else:
            label = instance.label

        field_details['label'] = label

        if field_type != FIELD_TYPES[14][0] and field_type != FIELD_TYPES[15][0]:
            field_details['placeholder'] = instance.placeholder
            field_details['validations'] = instance.validation_rule

        if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                field_type == FIELD_TYPES[12][0]:
            # Get Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
            field_options = []

            form_field_options = field.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0]).order_by(
                'option_order').all()
            for form_field_option in form_field_options:
                field_option = {
                    'value': form_field_option.id,
                    'label': form_field_option.label,
                }
                field_options.append(field_option)

            field_details['options'] = field_options

        if field_type == FIELD_TYPES[0][0] or field_type == FIELD_TYPES[1][0] or field_type == FIELD_TYPES[3][0] or \
                field_type == FIELD_TYPES[4][0] or field_type == FIELD_TYPES[5][0] or FIELD_TYPES[16][0]:
            # Text Box, Number, Email, Website URL, Dropdown, Phone No
            field_details['field_format'] = instance.field_format

        if field_type == FIELD_TYPES[14][0] or field_type == FIELD_TYPES[15][0]:
            # Heading, Paragraph
            field_details['content'] = instance.content
            field_details['content_size'] = instance.content_size
            field_details['content_alignment'] = instance.content_alignment

        fields_to_exclude = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]
        if field_type not in fields_to_exclude:
            # Update Field Label In Gsheet
            new_field_label = serializer.validated_data['label']
            gsheet = threading.Thread(target=update_field_label_in_gsheet, args=(old_field_label, new_field_label, form))
            gsheet.start()

        response_data['field_details'] = field_details
        return Response({"status": "success", "data": response_data, "msg": "Field Settings Updated Successfully"},
                        status=status.HTTP_200_OK)

@api_view(['GET'])
def get_form_payment_settings(req, form_id, payment_gateway=None, payment_mode=None):
    """
    Get Form Payment Settings
    - If Payment Gateway not provide, get Account Primary Payment Gateway
    - If Payment Mode not provide, get Form Primary Payment Mode
    """
    try:
        form = Form.objects.filter(id=form_id, type=FORM_TYPE[1][0]).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    zippy_form_account_id = form.account.id
    if payment_gateway is None:
        try:
            account = Account.objects.filter(id=zippy_form_account_id, status=ACCOUNT_STATUS[1][0]).get()
            payment_gateway = account.primary_payment_gateway

            _is_payment_collect_enabled = account.is_payment_collect_enabled
            if not _is_payment_collect_enabled:
                msg = "Payment settings cannot be updated because Account Payment Settings is disabled"
                return Response({"status": 'error', 'msg': msg}, status=status.HTTP_400_BAD_REQUEST)

        except Account.DoesNotExist:
            msg = "Account Does Not Exist"
            return Response({"status": 'error', 'msg': msg}, status=status.HTTP_400_BAD_REQUEST)
    else:
        _is_valid_payment_gateway = False
        for gateway in PAYMENT_GATEWAYS:
            if gateway[0] == payment_gateway:
                _is_valid_payment_gateway = True
                break
        if not _is_valid_payment_gateway:
            return Response({"status": 'error', 'msg': "Invalid Payment GateWay"}, status=status.HTTP_400_BAD_REQUEST)

    if payment_mode is None:
        payment_mode = form.primary_payment_mode
    else:
        _is_valid_payment_mode = False
        for mode in PAYMENT_MODE:
            if mode[0] == payment_mode:
                _is_valid_payment_mode = True
                break
        if not _is_valid_payment_mode:
            return Response({"status": 'error', 'msg': "Invalid Payment Mode"}, status=status.HTTP_400_BAD_REQUEST)


    form_payment_setting = form.form_payment_settings.filter(payment_gateway=payment_gateway, payment_mode=payment_mode).first()

    response_data = {}
    if form_payment_setting:
        response_data['id'] = form_payment_setting.id
        response_data['account_id'] = form_payment_setting.account.id
        response_data['payment_gateway'] = payment_gateway
        response_data['payment_type'] = form_payment_setting.payment_type
        response_data['payment_mode'] = form_payment_setting.payment_mode
        response_data['currency'] = form_payment_setting.currency
        response_data['price'] = form_payment_setting.price
        response_data['dynamic_price_field'] = form_payment_setting.dynamic_price_field
        response_data['tax_enabled'] = form_payment_setting.tax_enabled
        response_data['tax_display_name'] = form_payment_setting.tax_display_name
        response_data['tax'] = form_payment_setting.tax
        response_data['redirect_url'] = form_payment_setting.redirect_url

        if form_payment_setting.payment_gateway == PAYMENT_GATEWAYS[0][0]:
            application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])

            response_data['stripe'] = {}
            response_data['stripe']['connect_url'] = get_stripe_connect_url(payment_mode)
            if application_type == APPLICATION_TYPE[1][0]:
                is_stripe_connected = AccountPaymentSettings.objects.filter(account=form_payment_setting.account.id,
                                                                            payment_gateway=form_payment_setting.payment_gateway,
                                                                            payment_mode=form_payment_setting.payment_mode).exists()

                response_data['stripe']['show_connect'] = True
                response_data['stripe']['is_connected'] = is_stripe_connected
            else:
                response_data['stripe']['show_connect'] = False
                response_data['stripe']['is_connected'] = False

        # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here
    else:
        response_data['id'] = ''
        response_data['account_id'] = zippy_form_account_id
        response_data['payment_gateway'] = payment_gateway
        response_data['payment_type'] = PAYMENT_TYPE[0][0]
        response_data['payment_mode'] = payment_mode
        response_data['currency'] = ''
        response_data['price'] = ''
        response_data['dynamic_price_field'] = None
        response_data['tax_enabled'] = False
        response_data['tax_display_name'] = ""
        response_data['tax'] = ''
        response_data['redirect_url'] = ''

        if payment_gateway == PAYMENT_GATEWAYS[0][0]:
            application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])

            response_data['stripe'] = {}
            response_data['stripe']['connect_url'] = get_stripe_connect_url(payment_mode)
            if application_type == APPLICATION_TYPE[1][0]:
                is_stripe_connected = AccountPaymentSettings.objects.filter(account=zippy_form_account_id,
                                                                            payment_gateway=payment_gateway,
                                                                            payment_mode=payment_mode).exists()

                response_data['stripe']['show_connect'] = True
                response_data['stripe']['is_connected'] = is_stripe_connected
            else:
                response_data['stripe']['show_connect'] = False
                response_data['stripe']['is_connected'] = False

    return Response({"status": "success", "data": response_data},status=status.HTTP_200_OK)

@api_view(['POST'])
def update_form_payment_settings(req, form_id):
    """
    Update Form Payment Settings
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    _is_payment_collect_enabled = form.account.is_payment_collect_enabled
    if not _is_payment_collect_enabled:
        msg = "Payment settings cannot be updated because Account Payment Settings is disabled"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    form_type_check = form.type
    if form_type_check == FORM_TYPE[0][0]:
        msg = "Standard Form not allowed to update payment settings"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])

    is_payment_settings_updated_first_time = True

    selected_payment_gateway = req.data.get('payment_gateway', '')
    selected_payment_mode = req.data.get('payment_mode', '')
    selected_payment_type = req.data.get('payment_type', '')
    dynamic_price_type_check = True

    form_payment_settings = None
    if selected_payment_gateway and selected_payment_mode:
        form_payment_settings = FormPaymentSettings.objects.filter(form=form_id, payment_gateway=selected_payment_gateway, payment_mode=selected_payment_mode).first()

    if form_payment_settings:
        # Update Form Payment Settings

        old_payment_type = form_payment_settings.payment_type
        if old_payment_type == PAYMENT_TYPE[1][0] and selected_payment_type == PAYMENT_TYPE[1][0]:
            dynamic_price_type_check = False

        is_payment_settings_updated_first_time = False
        old_price = form_payment_settings.price
        old_tax = form_payment_settings.tax
        serializer = FormPaymentSettingsSerializer(form_payment_settings, data=req.data)
    else:
        # Create Form Payment Settings
        serializer = FormPaymentSettingsSerializer(data=req.data)

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        account = form.account
        is_payment_collect_enabled = account.is_payment_collect_enabled

        if is_payment_collect_enabled:
            # If Payment Collect Enabled For Account
            connected_account_id = ""

            if selected_payment_gateway == PAYMENT_GATEWAYS[0][0]:
                # Handle for stripe
                secret_key = get_stripe_secret_key(selected_payment_mode)
                if not secret_key:
                    msg = "Please add Stripe Secret Key to the application before updating Payment Settings"
                    return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

            # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

            if application_type == APPLICATION_TYPE[1][0]:
                # If the application configuried as "saas" application
                account_payment_settings = account.account_payment_settings.filter(payment_gateway=selected_payment_gateway, payment_mode=selected_payment_mode).first()
                if account_payment_settings and account_payment_settings.key:
                    connected_account_id = account_payment_settings.key
                else:
                    if selected_payment_gateway == PAYMENT_GATEWAYS[0][0]:
                        # Handle error for Stripe
                        msg = "Please Connect to your Stripe Account before updating Payment Settings"
                        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

                        msg = "Secret Key required"
                        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

            if selected_payment_type == PAYMENT_TYPE[0][0]:
                    application_fee_amount = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_APPLICATION_FEE_AMOUNT',
                                                     DEFAULT_STRIPE_APPLICATION_FEE_AMOUNT)
                    if application_fee_amount > int(serializer.validated_data.get('price')):
                        return Response({
                            "status": "validation_error",
                            "data": {"price": ["Price should not be less than the Application Fees amount"]}
                        }, status=status.HTTP_400_BAD_REQUEST)

        instance = serializer.save()

        # Update Primary Payment Mode for the from
        form.primary_payment_mode = selected_payment_mode
        form.save()

        if is_payment_collect_enabled:
            # If Payment Collect Enabled For Account

            # If Payment Type is "Fixed Price" or "Dynamic Price"
            payment = Payment(selected_payment_gateway, secret_key, application_type, connected_account_id)
            if is_payment_settings_updated_first_time:
                # Save Product, Price, Tax in Stripe - When settings created first time
                created_product  = payment.create_product(form.name)
                created_price = payment.create_price(created_product, instance.payment_type, instance.currency, instance.price)
                created_tax = ""
                if instance.tax_enabled and instance.tax:
                    created_tax = payment.create_tax(instance.tax_display_name, instance.tax)

                # Save Product ID, Price ID, Tax Rate ID in DB
                instance.stripe_product_id = created_product
                instance.stripe_price_id = created_price
                instance.stripe_tax_rate_id = created_tax
                instance.save()
            else:
                # Update Price in Stripe - When settings updated(second time...)
                if selected_payment_type == PAYMENT_TYPE[0][0]:
                    # Handle for Fixed Price
                    new_price = serializer.validated_data['price']
                    if old_price == '':
                        # If Payment Type updated from Dynamic Price to Fixed Price
                        update_price = payment.update_price(instance.stripe_product_id, instance.payment_type, instance.currency,
                                                             instance.price, instance.stripe_price_id)
                        instance.stripe_price_id = update_price
                        instance.save()
                    elif float(old_price) != float(new_price):
                        # If Payment Type is Fixed Price(no payment type changed) & if price changed
                        update_price = payment.update_price(instance.stripe_product_id, instance.payment_type,
                                                            instance.currency, instance.price, instance.stripe_price_id)
                        # Update Price ID in DB
                        instance.stripe_price_id = update_price
                        instance.save()
                else:
                    # Handle for Dynamic Price
                    if dynamic_price_type_check:
                        # If Payment Type updated from Fixed Price to Dynamic Price
                        update_price = payment.update_price(instance.stripe_product_id, instance.payment_type,
                                                            instance.currency, instance.price, instance.stripe_price_id)
                        # Update Price ID in DB
                        instance.stripe_price_id = update_price
                        instance.price = ''
                        instance.save()

                if instance.tax_enabled and instance.tax:
                    # If tax enabled & tax added
                    if not instance.stripe_tax_rate_id:
                        # If tax not created previously, newly created on update
                        # Create Tax Rate ID in Stripe
                        created_tax = payment.create_tax(instance.tax_display_name, instance.tax)
                        # Create Tax Rate ID in DB
                        instance.stripe_tax_rate_id = created_tax
                        instance.save()
                    else:
                        # If tax created previously, tax changed
                        new_tax = serializer.validated_data['tax']
                        if float(old_tax) != float(new_tax):
                            # Update Tax Rate ID in Stripe
                            update_tax = payment.update_tax(instance.tax_display_name, instance.tax,
                                                            instance.stripe_tax_rate_id)
                            # Update Tax Rate ID in DB
                            instance.stripe_tax_rate_id = update_tax
                            instance.save()

        response_data = {}
        response_data['id'] = instance.id

        return Response({"status": "success", "data": response_data, "msg": "Form Payment Settings Updated Successfully"},
                        status=status.HTTP_200_OK)



@api_view(['DELETE'])
def delete_field(req, form_id, field_id):
    """
    Soft delete field
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    try:
        field = form.form_fields.filter(id=field_id).exclude(status=FORM_FIELD_STATUS[0][0]).get()
    except FormField.DoesNotExist:
        msg = "Invalid Form Field ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    #  Soft delete form field
    field.status = FORM_FIELD_STATUS[0][0]
    field.save()

    fields_to_exclude = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]
    if field.field_type not in fields_to_exclude:
        # Remove field from Gsheet
        gsheet = threading.Thread(target=remove_field_from_gsheet, args=(field.label, form))
        gsheet.start()

    response_data = {'field': {}}

    response_data['field']['id'] = field.id

    return Response({"status": "success", "data": response_data, "msg": "Form Field Deleted Successfully"},
                    status=status.HTTP_200_OK)

@api_view(['GET'])
def get_form_active_number_fields(req, form_id):
    """
    Get Form Active Number Fields
    """
    try:
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    form_fields = form.form_fields.filter(field_type=FIELD_TYPES[3][0], status=FORM_FIELD_STATUS[1][0])

    active_number_fields = []
    for form_field in form_fields:
        temp = {}
        temp['id'] = form_field.id
        temp['label'] = form_field.label

        active_number_fields.append(temp)

    return Response({"status": "success", "data": active_number_fields}, status=status.HTTP_200_OK)

@api_view(['POST'])
def form_payment_settings_stripe_connect(req):
    """
    Form Payment Settings - Stripe Connect
    """
    code = req.data.get('code', None)
    form = req.data.get('form', None)
    payment_mode = req.data.get('payment_mode', None)

    # Validate User Inputs
    blank_errors = {}
    if code == '':
        blank_errors['code'] = ['This field may not be blank']
    if form == '':
        blank_errors['form'] = ['This field may not be blank']
    if payment_mode == '':
        blank_errors['payment_mode'] = ['This field may not be blank']

    if len(blank_errors) > 0:
        return Response({"status": "validation_error", "data": blank_errors},
                        status=status.HTTP_400_BAD_REQUEST)

    field_required_errors = {}
    if not code:
        field_required_errors['code'] = ['This field is required']
    if not form:
        field_required_errors['form'] = ["This field is required"]
    if not payment_mode:
        field_required_errors['payment_mode'] = ['This field is required']

    if len(field_required_errors)>0:
        return Response({"status": "validation_error", "data": field_required_errors}, status=status.HTTP_400_BAD_REQUEST)

    try:
        form = Form.objects.filter(id=form).exclude(Q(status=FORM_STATUS[0][0]) | Q(status=FORM_STATUS[2][0])).get()
    except Form.DoesNotExist:
        return Response({"status": "validation_error", "data": {"form": ['Invalid Form ID']}}, status=status.HTTP_400_BAD_REQUEST)

    is_valid_payment_mode = False
    for mode in PAYMENT_MODE:
        if mode[0] == payment_mode:
            is_valid_payment_mode = True
            break
    if not is_valid_payment_mode:
        return Response({"status": "validation_error", "data": {"payment_mode": ['Invalid Payment Mode']}}, status=status.HTTP_400_BAD_REQUEST)

    secret_key = get_stripe_secret_key(payment_mode)

    account = form.account
    zippyform_account = account.id
    is_payment_collect_enabled = account.is_payment_collect_enabled

    if is_payment_collect_enabled:
        stripe_connect_response = stripe_connect(secret_key, code)

        if stripe_connect_response['stripe_user_id'] == "":
            return Response({"status": "error",
                             "data": str(stripe_connect_response['error'])},
                            status=status.HTTP_400_BAD_REQUEST)

        stripe_account_id = stripe_connect_response['stripe_user_id']

        if payment_mode == PAYMENT_MODE[0][0]:
            accountpaymentsettings = AccountPaymentSettings.objects.create(account_id=zippyform_account,
                                                  payment_gateway=PAYMENT_GATEWAYS[0][0],
                                                  payment_mode=PAYMENT_MODE[0][0],
                                                  key=stripe_account_id,
                                                  )
        elif payment_mode == PAYMENT_MODE[1][0]:
            accountpaymentsettings = AccountPaymentSettings.objects.create(account_id=zippyform_account,
                                                  payment_gateway=PAYMENT_GATEWAYS[0][0],
                                                  payment_mode=PAYMENT_MODE[1][0],
                                                  key=stripe_account_id,
                                                  )

        return Response({"status": "success", "msg": "Stripe Connected Successfully"},
                        status=status.HTTP_200_OK)
    else:
        return Response({"status": "error", "msg": 'Please enable Payment Collect on your Account before connecting to Stripe'},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_payment_gateway_webhook(req):
    """
    Create Webhook in Payment Gateway
    """
    payment_gateway = req.data.get('payment_gateway', '')
    payment_mode = req.data.get('payment_mode', '')
    webhook_url = req.data.get('webhook_url', '')

    errors = {}
    if payment_mode == '':
        errors["payment_mode"] = ["This field is required"]
    else:
        is_valid = False
        for mode in PAYMENT_MODE:
            if payment_mode in mode:
                is_valid = True
        if not is_valid:
            errors["payment_mode"] = ["Invalid Payment Mode"]

    if webhook_url == '':
        errors["webhook_url"] = ["This field is required"]
    else:
        is_valid = False
        if "http://" in webhook_url:
            is_valid = True
        elif "https://" in webhook_url:
            is_valid = True
        if not is_valid:
            errors["webhook_url"] = ["Enter a valid URL"]

    if payment_gateway == '':
        errors["payment_gateway"] = ["This field is required"]
    else:
        is_valid = False
        for PAYMENT_GATEWAY in PAYMENT_GATEWAYS:
            if payment_gateway in PAYMENT_GATEWAY:
                is_valid = True
        if not is_valid:
            errors["payment_gateway"] = ["Invalid Payment Gateway"]

    if errors !={}:
        return Response({"status": "validation_error", "data": errors}, status=status.HTTP_400_BAD_REQUEST)

    if payment_gateway == PAYMENT_GATEWAYS[0][0]:
        # Handle for Stripe
        secret_key = get_stripe_secret_key(payment_mode)

    # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

    application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])
    payment = Payment(payment_gateway, secret_key, application_type)

    try:
        created_webhook = payment.create_webhook(webhook_url)
    except Exception as e:
        return Response({'status': "error", 'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    PaymentGatewayWebhook.objects.create(payment_gateway=payment_gateway, payment_mode=payment_mode,
                                             webhook_reference_id=created_webhook)

    msg = "Webhook Created in {payment_gateway} Successfully".format(payment_gateway = payment_gateway)
    return Response({'status': 'success', 'data': msg}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_payment_gateway_webhook_list(req, payment_gateway, payment_mode):
    """
    Get list of all Webhook from Payment Gateway
    """
    errors = {}

    is_valid = False
    for mode in PAYMENT_MODE:
        if payment_mode in mode:
            is_valid = True
    if not is_valid:
        errors["payment_mode"] = ["Invalid Payment Mode"]

    is_valid = False
    for PAYMENT_GATEWAY in PAYMENT_GATEWAYS:
        if payment_gateway in PAYMENT_GATEWAY:
            is_valid = True
    if not is_valid:
        errors["payment_gateway"] = ["Invalid Payment Gateway"]

    if errors !={}:
        return Response({"status": "validation_error", "data": errors}, status=status.HTTP_400_BAD_REQUEST)

    if payment_gateway == PAYMENT_GATEWAYS[0][0]:
        # Handle for Stripe
        secret_key = get_stripe_secret_key(payment_mode)

    # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

    application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])
    payment = Payment(payment_gateway, secret_key, application_type)
    webhooks = payment.list_webhook()

    return Response({'status': 'success', 'data': webhooks}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_webhook(req):
    """
    Create Webhook
    """
    form_submission_event_mapped_forms = json.loads(req.data.get('forms', "[]"))
    serializer = WebhookSerializer(data=req.data, context={'forms': form_submission_event_mapped_forms })

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        instance = serializer.save()

        # Bulk Create Webhook Forms
        webhook_forms = []
        for form_id in form_submission_event_mapped_forms:
            webhook_form = WebhookForm(webhook=instance, form_id=form_id, event_new_form_created=serializer.validated_data.get('event_new_form_created', False),
                            event_form_submit=serializer.validated_data.get('event_form_submit', False))
            webhook_forms.append(webhook_form)
        WebhookForm.objects.bulk_create(webhook_forms)

        response_data = {}
        response_data['id'] = instance.id

        return Response({"status": "success", "data": response_data, "msg": "Webhook Created Successfully"},
                        status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAccountActive])
def webhook_list(req):
    """
    Get list of active & inactive webhooks mapped to the account
    """
    account_id = req.headers.get('ZF-SECRET-KEY')

    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    search_by_keyword = req.GET.get('search', None)
    page_size = req.GET.get('page_size', DEFAULT_PAGE_SIZE)

    # Get only non deleted Webhooks
    webhooks = Webhook.objects.filter(account_id=account_id).exclude(status=WEBHOOK_STATUS[0][0]).order_by(
        '-created_date')
    if search_by_keyword:
        webhooks = webhooks.filter(Q(endpoint_url__icontains=search_by_keyword))

    paginator = Paginator(webhooks, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page"

        return Response({"status": "error", "msg": "Invalid Page", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each Webhook
        for webhook in page_obj.object_list:
            single_row_entry = {}
            single_row_entry['id'] = webhook.id
            single_row_entry['endpoint_url'] = webhook.endpoint_url
            single_row_entry['description'] = webhook.description
            single_row_entry['account'] = webhook.account.id
            single_row_entry['status'] = webhook.status
            single_row_entry['status_text'] = WEBHOOK_STATUS_DETAILS[webhook.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def webhook_detail(req, webhook_id):
    """
    Webhook Detail
    """
    webhook = Webhook.objects.filter(id=webhook_id).exclude(status=WEBHOOK_STATUS[0][0]).select_related(
        'account').first()
    if webhook:
        forms = []
        webhook_forms = webhook.webhook_form.all()
        for webhook_form in webhook_forms:
            forms.append({"form_id": webhook_form.form.id, "form_name": webhook_form.form.name,
                          "form_description": webhook_form.form.description})

        webhook_detail_info = {
            "id": webhook.id,
            'endpoint_url': webhook.endpoint_url,
            "account": webhook.account.id,
            "description": webhook.description,
            "event_new_form_created": webhook.event_new_form_created,
            "event_form_submit": webhook.event_form_submit,
            "webhook_forms": forms,
            'status': webhook.status,
            'status_text': WEBHOOK_STATUS_DETAILS[webhook.status]
        }
        return Response({"status": "success", "data": webhook_detail_info}, status=status.HTTP_200_OK)
    else:
        msg = "Invalid Webhook ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_webhook(req, webhook_id):
    """
    Update Webhook
    """
    try:
        # Update Webhook
        webhook = Webhook.objects.filter(id=webhook_id).exclude(status=WEBHOOK_STATUS[0][0]).get()
    except Exception as e:
        msg = "Invalid Webhook ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    webhook_status = req.data.get('status', False)
    if not webhook_status:
        return Response({"status": "validation_error", "data": {"status": ['This field is required']}},
                        status=status.HTTP_400_BAD_REQUEST)

    form_submission_event_mapped_forms = json.loads(req.data.get('forms', "[]"))
    serializer = WebhookSerializer(webhook, data=req.data, context={'forms': form_submission_event_mapped_forms })

    if not serializer.is_valid():
        return Response({"status": "validation_error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    else:
        webhook.endpoint_url = serializer.validated_data.get('endpoint_url')
        webhook.description = serializer.validated_data.get('description')
        webhook.event_new_form_created = serializer.validated_data.get('event_new_form_created', False)
        webhook.event_form_submit = serializer.validated_data.get('event_form_submit', False)
        webhook.status = serializer.validated_data.get('status')
        webhook.save()

        # Delete All Current WebhookForm Of Webhook
        webhook.webhook_form.all().delete()

        # Bulk Create Webhook Forms
        webhook_forms = []
        for form_id in form_submission_event_mapped_forms:
            webhook_form = WebhookForm(webhook=webhook, form_id=form_id, event_new_form_created=serializer.validated_data.get('event_new_form_created', False),
                            event_form_submit=serializer.validated_data.get('event_form_submit', False))
            webhook_forms.append(webhook_form)
        WebhookForm.objects.bulk_create(webhook_forms)

        response_data = {'data': {}}
        response_data['data']['id'] = webhook.id
        response_data['data']['endpoint_url'] = webhook.endpoint_url
        response_data['data']['description'] = webhook.description
        response_data['data']['event_new_form_created'] = webhook.event_new_form_created
        response_data['data']['event_form_submit'] = webhook.event_form_submit

        return Response({"status": "success", "data": response_data, "msg": "Webhook Updated Successfully"},
                        status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_webhook(req, webhook_id):
    """
    Soft Delete Webhook
    """
    try:
        webhook = Webhook.objects.filter(id=webhook_id).exclude(status=WEBHOOK_STATUS[0][0]).get()
    except Webhook.DoesNotExist:
        data = "Invalid Webhook ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    # Soft delete webhook
    webhook.status = WEBHOOK_STATUS[0][0]
    webhook.save()
    response_data = {'webhook': {}}
    response_data['webhook']['id'] = webhook.id

    return Response({"status": "success", "data": response_data, "msg": "Webhook Deleted Successfully"},
                    status=status.HTTP_200_OK)

@api_view(['POST'])
def update_webhook_status(req, webhook_id):
    """
    Update webhook status
    * Active to InActive
    * InActive to Active
    """
    try:
        webhook = Webhook.objects.filter(id=webhook_id).exclude(status=WEBHOOK_STATUS[0][0]).get()
    except Webhook.DoesNotExist:
        data = "Invalid Webhook ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    webhook_status = webhook.status
    if webhook_status == WEBHOOK_STATUS[1][0]:
        webhook.status = WEBHOOK_STATUS[2][0]
    elif webhook_status == WEBHOOK_STATUS[2][0]:
        webhook.status = WEBHOOK_STATUS[1][0]

    webhook.save()
    response_data = {'webhook': {}}
    response_data['webhook']['id'] = webhook.id
    response_data['webhook']['status'] = webhook.status

    return Response({"status": "success", "data": response_data, "msg": "Update Webhook Status Successfully"},
                    status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAccountActive])
def dynamic_form_list(req):
    """
    Get list of active forms mapped to the account
    """
    response_data = {'list': {}}

    page = req.GET.get('page', 1)
    search_by_keyword = req.GET.get('search', None)
    filter_by_type = req.GET.get('type', None)
    page_size = req.GET.get('page_size', DEFAULT_PAGE_SIZE)

    account_id = req.headers['ZF-SECRET-KEY']

    # Get only active forms
    forms = Form.objects.filter(account_id=account_id).filter(status=FORM_STATUS[1][0]).order_by('-created_date')
    account = Account.objects.filter(id=account_id).first()
    account_timezone  = ""
    if account:
        account_timezone = account.timezone

    if search_by_keyword:
        forms = forms.filter(Q(name__icontains=search_by_keyword))
    if filter_by_type:
        forms = forms.filter(type=filter_by_type)

    paginator = Paginator(forms, page_size)
    page_obj = paginator.get_page(page)

    if int(page) > page_obj.paginator.num_pages:
        response_data['list']['per_page'] = 0
        response_data['list']['page'] = 0
        response_data['list']['total'] = 0
        response_data['list']['total_pages'] = 0
        response_data['list']['data'] = []
        response_data['list']['msg'] = "Invalid Page"

        return Response({"status": "error", "msg": "Invalid Page", "data": response_data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        data = []
        # Loop each form
        for form in page_obj.object_list:
            single_row_entry = {}
            single_row_entry['id'] = form.id
            single_row_entry['name'] = form.name
            single_row_entry['description'] = form.description
            single_row_entry['created_date'] = convert_utc_to_timezone(str(form.created_date), account_timezone).strftime("%m-%d-%Y")
            single_row_entry['status'] = form.status
            single_row_entry['status_text'] = FORM_STATUS_DETAILS[form.status]

            data.append(single_row_entry)

        response_data['list']['per_page'] = page_obj.paginator.per_page
        response_data['list']['page'] = page_obj.number
        response_data['list']['total'] = page_obj.paginator.count
        response_data['list']['total_pages'] = page_obj.paginator.num_pages
        response_data['list']['data'] = data

        return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)



@api_view(['GET'])
def dynamic_form_fields_mapped_to_form_step(req, form_id, step_id=None):
    """
    Frontend(Dynamic Form) - Active Field mapped to Form Step
    """
    try:
        # Get only non deleted Form
        form = Form.objects.filter(id=form_id).exclude(status=FORM_STATUS[0][0]).get()
    except Form.DoesNotExist:
        data = "Invalid Form ID"
        return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

    preview_mode = req.GET.get('preview', False)
    if form.status == FORM_STATUS[3][0]:
        if preview_mode:
            msg = "Form preview is available only after publishing"
        else:
            msg = "Form can be submitted only after publishing. Please contact admin."

        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)


    # Get all step mapped to form - Query not executed here
    form_steps = form.form_steps.filter(status=FORM_STEP_STATUS[1][0]).order_by('step_order')

    steps_with_active_fields = []
    for form_step in form_steps:
        step_has_fields = FormField.objects.filter(form_id=form_id, form_step=form_step.id,
                                                   status=FORM_FIELD_STATUS[1][0]).exists()
        if step_has_fields:
            step = {}
            step['id'] = form_step.id
            step['name'] = form_step.name
            step['description'] = form_step.description

            steps_with_active_fields.append(step)

    if step_id is None:
        # For first step
        if steps_with_active_fields:
            first_form_step = steps_with_active_fields[0]
            current_step = str(first_form_step['id'])
        else:
            current_step = None

            # If no fields mapped to the first step
            if preview_mode:
                data = "Preview requires at least one field to be mapped in the form"
            else:
                data = "Form submission requires at least one field to be mapped in the form"

            return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Check if the "step id" received from request is valid
        try:
            form.form_steps.filter(id=step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        except FormStep.DoesNotExist:
            data = "Invalid Form Step ID"
            return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)

        current_step = step_id

    form_fields = None

    if current_step:
        # Get only active fields
        form_fields = FormField.objects.filter(form_id=form_id).filter(form_step=current_step) \
            .filter(status=FORM_FIELD_STATUS[1][0]).order_by('field_order').prefetch_related('form_field_options')

        if not form_fields:
            # if no active fields available for the current step
            data = "No active fields mapped to the form step"

            return Response({"status": "error", "msg": data}, status=status.HTTP_400_BAD_REQUEST)


    steps = []
    fields = []

    response_data = {'action': "#", 'form': {}, 'steps': steps, 'fields': fields}

    response_data['form']['id'] = form.id
    response_data['form']['name'] = form.name
    response_data['form']['type'] = form.type
    response_data['form']['description'] = form.description
    response_data['form']['class_name'] = form.class_name
    response_data['form']['success_msg'] = form.success_msg

    for form_step in steps_with_active_fields:
        step = form_step
        if current_step == str(form_step['id']):
            step['is_current_step'] = True
        else:
            step['is_current_step'] = False

        steps.append(step)

    if form_fields:
        for form_field in form_fields:
            field_details = {
                'field_id': form_field.id,
                'field_type': form_field.field_type,
                'field_order': form_field.field_order,
                'class_name': form_field.field_size + " " + form_field.custom_class_name,
            }

            field_type = form_field.field_type

            fields_to_exclude_label = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]

            if field_type in fields_to_exclude_label:
                label= ''
            else:
                label = form_field.label

            field_details['label'] = label

            if field_type != FIELD_TYPES[14][0] and field_type != FIELD_TYPES[15][0]:
                field_details['placeholder'] = form_field.placeholder
                field_details['validations'] = form_field.validation_rule

            if field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[6][0] or field_type == FIELD_TYPES[7][0] or \
                    field_type == FIELD_TYPES[12][0]:
                # Get Options for Dropdown, Radio, Checkbox, MultiSelect Checkbox fields
                field_options = []

                form_field_options = form_field.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0]).order_by('option_order').all()
                for form_field_option in form_field_options:
                    field_option = {
                        'value': form_field_option.id,
                        'label': form_field_option.label,
                    }
                    field_options.append(field_option)

                field_details['options'] = field_options

            if field_type == FIELD_TYPES[0][0] or field_type == FIELD_TYPES[1][0] or field_type == FIELD_TYPES[3][0] or \
                    field_type == FIELD_TYPES[4][0] or field_type == FIELD_TYPES[5][0] or field_type == FIELD_TYPES[16][0]:
                # Text Box, Number, Email, Website URL, Dropdown, Phone No
                field_details['field_format'] = form_field.field_format

            if field_type == FIELD_TYPES[14][0] or field_type == FIELD_TYPES[15][0]:
                # Heading, Paragraph
                field_details['content'] = form_field.content
                field_details['content_size'] = form_field.content_size
                field_details['content_alignment'] = form_field.content_alignment

            fields.append(field_details)

        response_data['fields'] = fields
    else:
        response_data['fields'] = []

    return Response({"status": "success", "data": response_data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def submit_form(req, form_id, step_id, submission_id=None):
    """
    Frontend(Dynamic Form) - Submit Form
    """
    try:
        # Allow submit only for active form from frontend
        form = Form.objects.filter(id=form_id).filter(status=FORM_STATUS[1][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    _form_type = form.type
    account_timezone = form.account.timezone
    updated_at = ""
    payment_type = ""
    payment_mode = ""

    _is_payment_collect_enabled = form.account.is_payment_collect_enabled
    if _form_type == FORM_TYPE[1][0] and not _is_payment_collect_enabled:
        msg = "Form submission is restricted as the Account Payment setting remains disabled"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the "step id" received from request is valid
    try:
        current_step = form.form_steps.filter(id=step_id).filter(status=FORM_STEP_STATUS[1][0]).get()
        current_step_order = current_step.step_order
    except FormStep.DoesNotExist:
        msg = "Invalid Form Step ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    # Check if the form has any active previous step
    is_previous_step_exits = form.form_steps.filter(step_order__lt=current_step_order).filter(
        status=FORM_STEP_STATUS[1][0]).first()

    # If has previous step & Form Submission ID not provided - Form Submission ID required
    if is_previous_step_exits and submission_id is None:
        msg = "Form Submission ID Required"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    # Get only active fields mapped to the step
    form_fields = FormField.objects.filter(form_id=form_id).filter(form_step=step_id) \
        .filter(status=FORM_FIELD_STATUS[1][0])

    form_field_ids = []
    for form_field in form_fields:
        form_field_ids.append(form_field.id)

    # Validate all active fields mapped to the step
    validation = validate_form_fields(req, form_fields, req.data, step_id, submission_id)

    # Handle validation error & error
    if validation['status'] == 'validation_error' or  validation['status'] == 'error':
        return Response(validation, status=status.HTTP_400_BAD_REQUEST)

    # Handle validation success
    if submission_id is None:
        # Create Form Submission Entry
        form_submission = FormSubmission.objects.create(form=form)
    else:
        # Existing Form Submission Entry
        try:
            form_submission = FormSubmission.objects.filter(id=submission_id).get()
        except FormSubmission.DoesNotExist:
            msg = "Invalid Form Submission ID"
            return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    updated_at = convert_utc_to_timezone(str(form_submission.modified_date), account_timezone).strftime(
        "%m-%d-%Y %H:%M:%S")
    submission_reference = uuid.uuid4()

    form_data_for_gsheet = {}

    # Save form submission data against the form submission entry
    for form_data in req.data:
        form_data_key = form_data
        form_data_value = req.data[form_data]

        field_detail = FormField.objects.filter(id=form_data_key).filter(status=FORM_FIELD_STATUS[1][0]).first()

        # Save form submission data to respective column based on the field type
        if field_detail:
            form_submission_data = FormSubmissionData()
            form_submission_data.form_submission = form_submission
            form_submission_data.form_field = field_detail
            form_submission_data.form_field_type = field_detail.field_type
            form_submission_data.submission_reference = submission_reference

            if field_detail.field_type == FIELD_TYPES[0][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[1][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[2][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[3][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[4][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[5][0]:
                form_submission_data.dropdown_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[6][0]:
                form_submission_data.radio_field = form_data_value
            # elif field_detail.field_type == FIELD_TYPES[7][0]:
            #     form_submission_data.checkbox_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[8][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[9][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[10][0]:
                if validate_is_empty(form_data_value):
                    if submission_id:
                        # If empty value provided on edit, retain old value for file
                        previous_field_details = FormSubmissionData.objects.filter(form_submission=submission_id,
                                                                                   form_field=field_detail).last()
                        if previous_field_details:
                            form_submission_data.file_field = previous_field_details.file_field
                        else:
                            form_submission_data.file_field = ""
                    else:
                        form_submission_data.file_field = ""
                elif form_data_value == 'reset':
                    form_submission_data.file_field = ""
                else:
                    form_submission_data.file_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[11][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[12][0]:
                form_submission_data.multiselect_checkbox_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[13][0]:
                form_submission_data.text_field = form_data_value
            elif field_detail.field_type == FIELD_TYPES[16][0]:
                form_submission_data.text_field = form_data_value

            form_submission_data.save()

            #Gsheet
            if field_detail.field_type == FIELD_TYPES[12][0]:
                # Multi Checkbox
                _values = format_string_to_json_array(form_submission_data.multiselect_checkbox_field)
                if _values is not None:
                    _option_values = get_field_option_values(_values)
                    _option_values = ",".join(_option_values)
                    form_data_for_gsheet[field_detail.label] =  _option_values
                else:
                    form_data_for_gsheet[field_detail.label] = ""
            elif field_detail.field_type == FIELD_TYPES[10][0]:
                # File
                if form_submission_data.file_field:
                    form_data_for_gsheet[field_detail.label] = form_submission_data.file_field.url
                else:
                    form_data_for_gsheet[field_detail.label] = ""
            elif field_detail.field_type == FIELD_TYPES[6][0]:
                # Radio
                _value = form_submission_data.radio_field
                _option_value = get_field_option_value(_value)
                form_data_for_gsheet[field_detail.label] = _option_value
            elif field_detail.field_type == FIELD_TYPES[5][0]:
                    # Dropdown
                    _values = format_string_to_json_array(form_submission_data.dropdown_field)
                    _option_values = get_field_option_values(_values)
                    _option_values = ",".join(_option_values)
                    if _values is not None:
                        form_data_for_gsheet[field_detail.label] = _option_values
                    else:
                        form_data_for_gsheet[field_detail.label] = ""
            else:
                form_data_for_gsheet[field_detail.label] = form_data_value

    # Delete Last Entry Of Form Submission
    if submission_id:
        FormSubmissionData.objects.filter(form_submission=submission_id).filter(form_field__in=form_field_ids).exclude(
            submission_reference=submission_reference).delete()

    form_submission_status = form_submission.status

    next_step_exist = FormStep.objects.filter(form=form_id).filter(step_order__gt=current_step_order).filter(status=FORM_STEP_STATUS[1][0]).exists()
    if not next_step_exist:
        # Last Step

        payment_mode = None
        # Handle payment collection if form type is "payment form"
        if form.type == FORM_TYPE[1][0]:
            acct_id = form.account.id
            account = Account.objects.filter(id=acct_id, status=ACCOUNT_STATUS[1][0]).first()

            _is_payment_collect_enabled = False
            if account:
                _is_payment_collect_enabled = account.is_payment_collect_enabled

            if _is_payment_collect_enabled:
                zippy_form_account_id = account.id
                primary_payment_gateway = account.primary_payment_gateway

                if primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
                    # Handle for Stripe
                    secret_key = get_stripe_secret_key(form.primary_payment_mode)
                    if not secret_key:
                        return Response({
                            "status": "error",
                            "msg":"Payment Error: #00 Secret Key Missing"
                        }, status=status.HTTP_400_BAD_REQUEST)

                # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

                connected_account_id = ""
                primary_payment_mode = form.primary_payment_mode
                application_type = getattr(settings, 'ZF_APPLICATION_TYPE', APPLICATION_TYPE[0][0])
                if application_type == APPLICATION_TYPE[1][0]:
                    # If application configured as SaaS
                    account_payment_settings = AccountPaymentSettings.objects.filter(account=zippy_form_account_id,
                                                                                 payment_gateway=primary_payment_gateway,
                                                                                 payment_mode=primary_payment_mode).first()
                    if account_payment_settings and account_payment_settings.key:
                        payment_mode = account_payment_settings.payment_mode
                        connected_account_id = account_payment_settings.key
                    else:
                        # Handle error for all Payment Gateway
                        return Response({
                            "status": "error",
                            "msg": "Payment Error: Tenant Secret Key Missing"
                        }, status=status.HTTP_400_BAD_REQUEST)

                        # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here(Optional)
                        # (If custom logics require for Payment Gateway can be added here.)
                else:
                    # If application configured as Standalone
                    pass

                form_payment_settings = FormPaymentSettings.objects.filter(form=form_id, account=zippy_form_account_id,
                                                                           payment_gateway=primary_payment_gateway, payment_mode=primary_payment_mode).first()

                application_fee_amount = getattr(settings, 'ZF_PAYMENT_GATEWAY_STRIPE_APPLICATION_FEE_AMOUNT',
                                                 DEFAULT_STRIPE_APPLICATION_FEE_AMOUNT)

                if form_payment_settings:
                    currency = form_payment_settings.currency
                    price = form_payment_settings.price
                    tax_enabled = form_payment_settings.tax_enabled
                    payment_type = form_payment_settings.payment_type
                    after_payment_redirect_url = form_payment_settings.redirect_url
                    dynamic_price_field = form_payment_settings.dynamic_price_field
                    payment_type = form_payment_settings.payment_type
                    payment_mode = form_payment_settings.payment_mode

                    payment = Payment(primary_payment_gateway, secret_key, application_type, connected_account_id)

                    if primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
                        # Handle for Stripe
                        # stripe_product_id = form_payment_settings.stripe_product_id
                        stripe_price_id = form_payment_settings.stripe_price_id
                        stripe_tax_rate_id = form_payment_settings.stripe_tax_rate_id

                        if price:
                            if application_fee_amount > int(price):
                                        return Response({
                                            "status": "error",
                                            "data": {"Payment Error: Price should not be less than the Application Fees"}
                                         })

                        if tax_enabled:
                            # Hanlde for fixed price payment
                            line_items = [{"price": stripe_price_id, "quantity": 1, "tax_rates": [stripe_tax_rate_id]}]
                        else:
                            # Hanlde for fixed price payment
                            line_items = [{"price": stripe_price_id, "quantity": 1}]

                            # dynamic_price_field_id = dynamic_price_field.id
                            # user_entered_price = FormSubmissionData.objects.filter(form_submission=form_submission,form_field=dynamic_price_field_id).first()
                            # if user_entered_price and user_entered_price.text_field:
                            #     price = int(user_entered_price.text_field) * 100
                            #
                            #     if price:
                            #         if application_fee_amount > int(user_entered_price.text_field):
                            #             return Response({
                            #                 "status": "error",
                            #                 "data": {"Payment Error: Price should not be less than the Application Fees"}
                            #              })
                            #         else:
                            #             line_items = {"unit_amount":price, "currency": currency}

                        form_submission_payment_detail = FormSubmissionPaymentDetails()
                        form_submission_payment_detail.form_submission = form_submission
                        form_submission_payment_detail.payment_mode = payment_mode
                        form_submission_payment_detail.payment_type = payment_type
                        form_submission_payment_detail.save()

                        checkout = payment.checkout(payment_type, application_fee_amount, line_items,
                                                    after_payment_redirect_url, form_id, form_submission.id,
                                                    form_submission_payment_detail.id)

                        if checkout and checkout['client_secret'] == '':
                            # Handle Checkout Error

                            # Delete Form Submission Payment Detail created previously
                            form_submission_payment_detail = FormSubmissionPaymentDetails.object.filter(
                                id=form_submission_payment_detail.id).delete()

                            return Response({
                                "status": "error",
                                "data": "Payment Error: " + checkout['error']
                            }, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            # If no error in checkout - update form submission payment details
                            form_submission_payment_detail = FormSubmissionPaymentDetails.objects.filter(
                                id=form_submission_payment_detail.id)
                            if payment_type == PAYMENT_TYPE[0][0]:
                                # If Payment type is Fixed Price
                                if tax_enabled:
                                    tax_percentage = form_payment_settings.tax
                                    currency = form_payment_settings.currency
                                    form_submission_payment_detail.update(
                                        form_submission=form_submission,
                                        tax_percentage=tax_percentage,
                                        sub_total=price,
                                        currency=currency
                                    )
                                else:
                                    currency = form_payment_settings.currency
                                    form_submission_payment_detail.update(
                                        form_submission=form_submission,
                                        sub_total=float(price),
                                        currency=currency
                                    )
                            else:
                                # If Payment type is Dynamic Price
                                if tax_enabled:
                                    tax_percentage = form_payment_settings.tax
                                    currency = form_payment_settings.currency
                                    form_submission_payment_detail.update(
                                        form_submission=form_submission,
                                        tax_percentage=tax_percentage,
                                        currency=currency
                                    )
                                else:
                                    currency = form_payment_settings.currency
                                    form_submission_payment_detail.update(
                                        form_submission=form_submission,
                                        currency=currency
                                    )

                    # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here
                else:
                    return Response({
                        "status": "error",
                        "data": "Payment Error: Form Payment Settings not updated"
                    }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "status": "error",
                    "data": "Payment Error: Please enble payment on your account"
                }, status=status.HTTP_400_BAD_REQUEST)
        # Handle payment collection if form type is "payment form"

        form_submission_last_revision = form_submission.revision
        form_submission_last_api_accessed_count = form_submission.api_accessed_count

        form_submission_new_revision = form_submission_last_revision + 1
        form_submission.api_accessed_count = form_submission_last_api_accessed_count + 1
        form_submission.revision = form_submission_new_revision

        if form.type == FORM_TYPE[1][0]:
            # Payment Form
            form_submission.status = FORM_SUBMISSION_STATUS[3][0]
        else:
            # Standard Form
            form_submission.status = FORM_SUBMISSION_STATUS[1][0]

        form_submission.save()

        if form_submission_last_api_accessed_count == 1:
            _method = "save"
        else:
            _method = "update"

        # Event & Webhook - Form Submit
        event_data = {
            "event": "form.submit",
            "method": _method,
            "account": {"id": str(form.account.id), "meta_detail": form.account.meta_detail},
            "form": {"id": str(form.id), "meta_detail": form.meta_detail, "status": form.status, "status_text": FORM_STATUS_DETAILS[form.status]},
            "form_submission": {"id": str(form_submission.id), "revision": form_submission_last_revision, "is_last_step": True, "status": form_submission.status, "status_text": format_form_submission_status(form_submission.status, form.type)}
        }
        after_form_submit(event_data)
    else:
        form_submission_last_revision = form_submission.revision
        form_submission_last_api_accessed_count = form_submission.api_accessed_count

        form_submission.api_accessed_count = form_submission_last_api_accessed_count + 1
        form_submission.save()

        if form_submission_last_api_accessed_count == 1:
            _method = "save"
        else:
            _method = "update"

    form_data_for_gsheet["Status"] =  format_form_submission_status(form_submission.status, form.type)
    form_data_for_gsheet["Updated At"] = updated_at
    form_data_for_gsheet["Payment Type"] = PAYMENT_TYPE_DETAILS[payment_type]
    form_data_for_gsheet["Payment Mode"] = PAYMENT_MODE_DETAILS[payment_mode]
    form_data_for_gsheet["Total Amount Paid"] = ""

    # Send Form Data To Gsheet - On every form step submission
    gsheet = threading.Thread(target=send_form_data_to_gsheet,
                              args=(_method, form, str(form_submission.id), form_data_for_gsheet))
    gsheet.start()

    if form.type == FORM_TYPE[0][0]:
        # Standard Form
        response_data = {
            'submission_id': form_submission.id,
            'from_type': FORM_TYPE[0][0]
        }
    else:
        # Payment Form
        if next_step_exist:
            response_data = {
                'submission_id': form_submission.id,
                'from_type': FORM_TYPE[0][0]
            }
        else:
            if payment_mode:
                if primary_payment_gateway == PAYMENT_GATEWAYS[0][0]:
                    # Handle for stripe
                    public_key = get_stripe_public_key(payment_mode)

                # Payment Gateway - When Working On New Payment Gateway, Add New Payment Gateway Secret Key Here

                if public_key:
                    response_data = {
                        'submission_id': form_submission.id,
                        'from_type': FORM_TYPE[1][0],
                        'application_type': application_type,
                        'payment_gateway': primary_payment_gateway,
                        'client_secret': checkout['client_secret'],
                        'public_key': public_key,
                        'connected_account_id': connected_account_id
                    }
                else:
                    return Response({
                        "status": "error",
                        "msg": "Payment Error: #00 Public Key Missing"
                    })
            else:
                return Response({
                    "status": "error",
                    "data": "Payment Error: Account Payment Settings missing"
                })

    return Response({"status": "success", "data": response_data, "msg": "Form Submitted Successfully"},
                    status=status.HTTP_200_OK)


@api_view(['POST'])
def webhook_stripe(req):
    """
    Consume Payment Status from Stripe
    """
    form_id = req.data['data']['object']['metadata']['form_id']
    form_submission_id = req.data['data']['object']['metadata']['form_submission_id']
    form_submission_payment_detail_id = req.data['data']['object']['metadata']['form_submission_payment_detail_id']
    form_submission_currency = req.data['data']['object']['currency']
    form_submission_sub_total = req.data['data']['object']['amount_subtotal']
    form_submission_tax_amount = req.data['data']['object']['total_details']['amount_tax'] if req.data['data']['object']['total_details']['amount_tax'] else 0
    form_submission_total = req.data['data']['object']['amount_total']
    stripe_payment_status = req.data['data']['object']['status']

    try:
        form = Form.objects.filter(id=form_id).filter(status=FORM_STATUS[1][0]).get()
    except Form.DoesNotExist:
        msg = "Invalid Form ID"
        return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

    _method = "update"
    tax_percentage = None

    if form_submission_tax_amount > 0:
        tax_percentage = form_submission_tax_amount/(form_submission_sub_total / 100)

    form_submission = FormSubmission.objects.filter(id=form_submission_id).get()

    if stripe_payment_status == 'complete':
        # Handle if payment status is completed
        form_sumbission_dtails_status = FORM_SUBMISSION_STATUS[1][0]

        # Update form submission status
        form_submission.status = form_sumbission_dtails_status
        form_submission.save()

        # Log payment status against form submission - for suceess
        try:
            log_payment_status(form_submission, form_submission_payment_detail_id,form_submission_sub_total, form_submission_tax_amount, tax_percentage,
                            form_submission_total, form_submission_currency, stripe_payment_status)
        except Exception as e:
            print(str(e))

        # Get Form Submission Payment Details
        try:
            form_submission_payment_details = FormSubmissionPaymentDetails.objects.filter(id=form_submission_payment_detail_id).get()
        except FormSubmissionPaymentDetails.DoestNotExist:
            msg = "Invalid Form Submission Payment Detail ID"
            return Response({"status": "error", "msg": msg}, status=status.HTTP_400_BAD_REQUEST)

        # Update Total Amount Paid & Status to GSheet
        form_data_for_gsheet = {}
        form_data_for_gsheet['Total Amount Paid'] = form_submission_payment_details.total
        form_data_for_gsheet["Status"] =  format_form_submission_status(form_submission.status, form.type)
        gsheet = threading.Thread(target=send_form_data_to_gsheet,
                                  args=(_method, form, str(form_submission_id), form_data_for_gsheet))
        gsheet.start()
    else:
        # Log payment status against form submission - for not suceess
        try:
            log_payment_status(form_submission, form_submission_payment_detail_id, form_submission_sub_total, form_submission_tax_amount, tax_percentage,
                            form_submission_total, form_submission_currency, stripe_payment_status)
        except Exception as e:
            print(str(e))

    return Response({'status':'success'}, status= status.HTTP_200_OK)


@api_view(['POST'])
def bulk_import(request, field_id):
    """
    Import From Excel and Csv
    """
    if request.method == 'POST':
        field = FormField.objects.filter(id=field_id).exclude(status=FORM_FIELD_STATUS[0][0]).first()
        if not field:
            return Response({'status': 'error', 'data': "Invalid Field ID"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            last_form_field = FormFieldOption.objects.filter(form_field=field).last()
            fieldorder = last_form_field.option_order if last_form_field else 0

        try:
            import_sheet_request = request.FILES.get("import_sheet", None)

            if import_sheet_request is None:
                return Response({'status': 'validation_error', 'data': {"import_sheet": ["Please provide Excel or CSV to import"]}},
                                status=status.HTTP_400_BAD_REQUEST)

            file_type_allowed = ['csv', 'xlsx']
            file_parts = str(import_sheet_request).split(".")
            if file_parts[-1] not in file_type_allowed:
                return Response({'status': 'validation_error', 'data': {"import_sheet": ["Invalid file type."]}},
                                status=status.HTTP_400_BAD_REQUEST)

            sheet_datas, df = import_sheets(import_sheet_request, fieldorder, field, "index", 'not_gsheet')
            if df.empty:
                return Response(
                    {"status": "error",
                     "data": f"The {import_sheet_request.name} file uploaded is empty or contains only empty rows "
                             f"and columns."}, status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success", "data": "Options Imported Successfully"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "error", "data": "Bulk Upload Failed", "error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def bulk_import_options_from_gsheet(request, field_id):
    """
    Import Field Options From Gsheet
    """
    if request.method == 'POST':
        field = FormField.objects.filter(id=field_id).exclude(status=FORM_FIELD_STATUS[0][0]).first()
        if not field:
            return Response({'status': 'error', 'data': "Invalid Field ID"},
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            last_form_field = FormFieldOption.objects.filter(form_field=field).last()
            fieldorder = last_form_field.option_order if last_form_field else 0

        try:
            url = request.data.get("url", None)

            if url is None:
                return Response({'status': 'validation_error', 'data': {"url": ["Please provide gsheet URL"]}},
                                status=status.HTTP_400_BAD_REQUEST)

            # Extract the spreadsheet ID using a regular expression
            spreadsheet_id_match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
            if not spreadsheet_id_match:
                return Response({'status': 'validation_error', 'data': {"url": ['Invalid URL']}},
                                status=status.HTTP_400_BAD_REQUEST)

            sheet_datas, df = import_sheets(url, fieldorder, field)
            if df.empty:
                return Response(
                    {"status": "error", "data": f"The {url} provided is empty or contains only empty rows "
                                                f"and columns"}, status.HTTP_400_BAD_REQUEST)

            return Response({"status": "success", "data": "Options Imported Successfully"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "error", "data": "Bulk Upload Failed", "error": str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


def import_sheets(sheet, fieldorder, field, orient="records", type='gsheet', column_index=0):
    """
    Extract Data From Gsheet, Excel and Csv
    """
    if type == 'gsheet':
        url = sheet
        # Extract the spreadsheet ID using a regular expression
        spreadsheet_id_match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)

        spreadsheet_id = spreadsheet_id_match.group(1)
        df = pd.read_csv(f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv', usecols=[0])
        cleaned_data = df.drop_duplicates(keep='first').to_dict(orient=orient)
        headings = df.columns.tolist()
        column_values = [{'label': option[headings[0]], 'order': fieldorder + 1} for fieldorder, option in
                         enumerate(cleaned_data, start=fieldorder)]
        create_update_field_options(column_values, field)
        return cleaned_data, df
    else:
        try:
            import_sheet = sheet.read()
            file_encoding = chardet.detect(import_sheet)['encoding']
            import_sheet = import_sheet.decode(file_encoding)
            df = pd.read_csv(io.StringIO(import_sheet), usecols=[column_index])
            cleaned_data = df.drop_duplicates(keep='first').to_dict(orient=orient)
            headings = df.columns.tolist()

        except:
            # If it's not a CSV, try reading it as an Excel file
            df = pd.read_excel(sheet, usecols=[column_index])
            cleaned_data = df.drop_duplicates(keep='first').to_dict(orient=orient)
            print(cleaned_data)
            headings = df.columns.tolist()

        column_values = [{'label': option[headings[0]], 'order': fieldorder + 1} for fieldorder, option in
                         enumerate(cleaned_data.values(), start=fieldorder)]
        create_update_field_options(column_values, field)
        return cleaned_data, df

def log_payment_status(form_submission, form_submission_payment_detail_id, form_submission_sub_total, form_submission_tax_amount, tax_percentage, form_submission_total,currency, stripe_payment_status):
    """
    Log Payment Status
    """
    form_submission_payment_details = FormSubmissionPaymentDetails.objects.filter(id=form_submission_payment_detail_id).update(
        sub_total=form_submission_sub_total / 100,
        tax_amount=(form_submission_tax_amount / 100),
        total=(form_submission_total / 100),
        currency=currency,
        payment_gateway_status=stripe_payment_status
    )

def validate_form_fields(req, form_fields, req_data, step_id, submission_id):
    """
    Validate all fields mapped to the step, when submitting each form step
    """
    form_req_data = {}
    form_missing_fields = []
    field_labels = {}
    field_types = {}
    field_validation_rules = {}
    validation_errors = {}

    # Loop & format the request data
    for form_data in req_data:
        field_key = str(form_data)
        field_req_value = req_data[form_data]

        form_req_data[field_key] = field_req_value

    # Loop & get all the validation rules added for the fields
    for form_field in form_fields:
        field_key = str(form_field.id)
        field_label = form_field.label
        field_type = form_field.field_type
        field_validation_rule = form_field.validation_rule

        # if field is "dropdown, radio, multiselect checkbox"
        if field_type == FIELD_TYPES[5][0]:
            field_validation_rule.update({"dropdown": True})

        if field_type == FIELD_TYPES[6][0]:
            field_validation_rule.update({"radio": True})

        if field_type == FIELD_TYPES[12][0]:
            field_validation_rule.update({"multiselect_checkbox": True})

        field_labels[field_key] = field_label
        field_types[field_key] = field_type
        field_validation_rules[field_key] = field_validation_rule

        fields_to_exclude = [FIELD_TYPES[14][0], FIELD_TYPES[15][0]]
        if field_type not in fields_to_exclude:
            # Get list of fields missed on the request
            if field_key not in form_req_data:
                form_missing_fields.append(field_key)

    # Validate fields - Check if all the fields mapped for the step are present on the request
    if len(form_missing_fields) > 0:
        data = {}
        for form_missing_field in form_missing_fields:
            data[form_missing_field] = "This field is required"

        return {"status": "validation_error", "error_on": "current_step", "error_step_id": step_id,
                "data": data,
                "msg": "Some fields missed or wrongly provided on the request"}

    # Validate fields - Loop each request data & validate based on validation rules
    for data in form_req_data:
        field_key = data
        try:
            field_label = field_labels[field_key]
            field_validation_rule = field_validation_rules[field_key]
            field_value = form_req_data[field_key]
            field_type = field_types[field_key]
        except:
            return {"status": "error", "data": {"key": field_key}, "msg": "Invalid Field Key"}

        # Validate single field
        validation = validate_form_field(req, field_key, field_label, field_validation_rule, field_value, field_type, submission_id)
        if len(validation) != 0:
            # If single field has error
            validation_errors.update(validation)

    # Validate fields - If any of the fields mapped for the step has error
    if len(validation_errors) > 0:
        return {"status": "validation_error", "error_on": "current_step", "error_step_id": step_id, "data": validation_errors}

    return {"status": "success"}


def validate_form_field(req, field_key, field_label, field_validation_rule, field_value, field_type, submission_id):
    """
    Validate single field based on the validation rule
    """
    validation_error = {}

    if FIELD_RULES[0][0] in field_validation_rule:
        if field_validation_rule['required']:
            if field_type == FIELD_TYPES[10][0]:
                # If 'field_type' is file
                if submission_id:
                    # If file is required & user attempt to reset with empty value, throw error
                    if field_value == 'reset':
                        validation_error[field_key] = f"{field_label} may not be blank"
                        return validation_error

                    # If has file already uploaded, skip required validation
                    previous_formsubmission_data = FormSubmissionData.objects.filter(form_submission=submission_id).filter(form_field_id=field_key).first()
                    if not previous_formsubmission_data:
                        error = validate_is_empty(field_value)
                        if error:
                            validation_error[field_key] = f"{field_label} may not be blank"
                            return validation_error
            else:
                # If 'field_type' is not file
                error = validate_is_empty(field_value)
                if error:
                    validation_error[field_key] = f"{field_label} may not be blank"
                    return validation_error


    if FIELD_RULES[10][0] in field_validation_rule:
        if field_value and field_validation_rule['max_selection']:
            max_selection_allowed = field_validation_rule.get('max_selection', 1)
            formatted_input = format_string_to_json_array(field_value)
            if formatted_input is None:
                validation_error[field_key] = f"{field_label} is invalid"
                return validation_error
            else:
                validate_min = field_validation_rule['required']
                validate_max = True
                error = validate_min_max_selection(formatted_input, max_selection_allowed, validate_min, validate_max)
                if error == 1:
                    validation_error[field_key] = "Please select at least one choice"
                    return validation_error
                elif error == 2:
                    validation_error[field_key] = f"You already reached the maximum number of accepted choices({max_selection_allowed})"
                    return validation_error

    if FIELD_RULES[9][0] in field_validation_rule:
        if field_value and field_validation_rule['number']:
            decimal_places_allowed = field_validation_rule.get('decimal_places', 0)
            if not field_validation_rule['decimal']:
                # if field configured, not to have decimal places
                error = validate_is_number(field_value)
                if error:
                    validation_error[field_key] = f"{field_label} is invalid"
            else:
                formatted_field_value = parse_to_float(field_value)
                # if field configured, to have decimal - allow value with decimal & without decimal
                if formatted_field_value is None:
                    validation_error[field_key] = f"{field_label} is invalid"
                else:
                    if '.' in str(field_value):
                        # if field is decimal, check the decimal place is same as the decimal place configured
                        decimal_places = len(str(field_value).split(".")[1])
                        if decimal_places != decimal_places_allowed:
                            validation_error[field_key] = f"{field_label} should contain {decimal_places_allowed} decimal places"

            if validation_error:
                return validation_error

    if FIELD_RULES[1][0] in field_validation_rule:
        if field_value:
            minlength = field_validation_rule['minlength']
            error = validate_minlength(field_value, minlength, field_type)
            if error:
                validation_error[field_key] = f"{field_label} must contain atleast {minlength} characters"
                return validation_error

    if FIELD_RULES[2][0] in field_validation_rule:
        if field_value:
            maxlength = field_validation_rule['maxlength']
            error = validate_maxlength(field_value, maxlength, field_type)
            if error:
                validation_error[field_key] = f"{field_label} should not be greater than {maxlength} characters"
                return validation_error

    if FIELD_RULES[3][0] in field_validation_rule:
        if field_value:
            min_value = field_validation_rule['min']
            error = validate_min_value(field_value, min_value)
            if error:
                validation_error[field_key] = f"{field_label} should be equal or greater than {min_value}"
                return validation_error

    if FIELD_RULES[4][0] in field_validation_rule:
        if field_value:
            max_value = field_validation_rule['max']
            error = validate_max_value(field_value, max_value)
            if error:
                validation_error[field_key] = f"{field_label} should be equal or less than {max_value}"
                return validation_error

    if FIELD_RULES[5][0] in field_validation_rule:
        if field_value  and field_validation_rule['email']:
            error = validate_is_email(field_value)
            if error:
                validation_error[field_key] = f"{field_label} is invalid"
                return validation_error

    if FIELD_RULES[6][0] in field_validation_rule:
        if field_value and field_validation_rule['url']:
            error = validate_is_url(field_value)
            if error:
                validation_error[field_key] = f"{field_label} is invalid"
                return validation_error

    if FIELD_RULES[7][0] in field_validation_rule:
        if field_value and field_validation_rule['date']:
            date_format_allowed = field_validation_rule.get('date_format', '')
            error = validate_is_date(field_value, date_format_allowed)
            if error:
                validation_error[field_key] = f"{field_label} is invalid"
                return validation_error

    if FIELD_RULES[8][0] in field_validation_rule:
        if field_value and field_validation_rule['unique']:
            error = validate_is_unique(field_value, field_key, field_type, submission_id)
            if error:
                validation_error[field_key] = f"{field_label} has been already taken"
                return validation_error

    if FIELD_RULES[11][0] in field_validation_rule:
        if field_validation_rule['file']:
            _validate_file = True

            if field_validation_rule['required']:
               # if the field is required - no value submitted but already as a value, skip this validation rule
               if not field_value and submission_id:
                    previous_formsubmission_data = FormSubmissionData.objects.filter(
                            form_submission=submission_id).filter(form_field_id=field_key).first()
                    if previous_formsubmission_data:
                        _validate_file = False
            else:
                # if the field is not required - no value submitted skip this validation rule
                if not field_value:
                    _validate_file = False

            if _validate_file:
                # if the field has value
                error = validate_is_file(field_key, req)
                if error:
                    # if file added is not valid file
                    string_data = req.data.get(field_key, None)
                    if string_data != 'reset':
                        if string_data != "":
                            # if text provided, with value apart from "reset" throw error
                            validation_error[field_key] = "InValid Data"
                            return validation_error
                        else:
                            # if empty file submitted
                            validation_error[field_key] = "No file Uploaded"
                            return validation_error
                else:
                    # if file added is valid file, validate extension
                    file_extensions_allowed = field_validation_rule['file_extensions_allowed']
                    invalid_file_error = validate_file_extension(field_value, file_extensions_allowed)
                    if invalid_file_error:
                        allowed_file_extensions = ", "
                        allowed_file_extensions = allowed_file_extensions.join(file_extensions_allowed)
                        validation_error[field_key] = f"Upload only {allowed_file_extensions} file"
                        return validation_error
                    else:
                        # if file added is with valid extension, validate file size
                        file_max_size_allowed = field_validation_rule.get('file_max_size_mb', 0)
                        invalid_file_size_error = validate_file_size(field_value, file_max_size_allowed)
                        if invalid_file_size_error:
                            # if file's size is greater than the allowed file size
                            validation_error[field_key] = f"Upload file smaller than {file_max_size_allowed}MB"
                            return validation_error

    if FIELD_RULES[12][0] in field_validation_rule:
        if field_value and field_validation_rule['time']:
            time_format_allowed = field_validation_rule.get('time_format', '')
            error = validate_is_time(field_value, time_format_allowed)
            if error:
                validation_error[field_key] = f"{field_label} is invalid"
                return validation_error

    return validation_error

def parse_to_float(value):
    """
    Parse the value to float
    """
    try:
        parsed_value = float(value)
    except:
        parsed_value = None

    return parsed_value

def format_string_to_json_array(string):
    """
    Format string to json array
    """
    formatted_string = None
    try:
        json_value = json.loads(string)
        if type(json_value) is list:
            formatted_string = json_value
        else:
            formatted_string = None
    except:
        formatted_string = None

    return formatted_string

def create_update_field_options(options, field_instance):
    """
    Create or Update Field Options
    """
    options_to_create = []
    options_to_edit = {}
    options_to_edit__id = []

    # loop all the form field options from request
    for option in options:
        _id = option.get('value', '')
        label = option.get('label', '')
        order = option.get('order', 0)
        if _id:
            options_to_edit[_id] = {'label': label, 'order': order}
            options_to_edit__id.append(_id)
        else:
            options_to_create.append(option)

    # Edit or Delete - Option

    form_field_options = field_instance.form_field_options.filter(status=FORM_FIELD_OPTION_STATUS[1][0])

    # loop all the form field options from DB with status "active", update or soft delete
    for form_field_option in form_field_options:
        option__id = str(form_field_option.id) # DB - Option ID

        if option__id in options_to_edit__id:
            req__option = options_to_edit[option__id] #get option received from request
            req__option_label = req__option['label']
            req__option_order = req__option['order']
            # Update Label & Order if modified
            if form_field_option.label != req__option_label or form_field_option.option_order != req__option_order:
                form_field_option.label = req__option_label
                form_field_option.option_order = req__option_order
                form_field_option.save()
        else:
            # Soft Delete Option
            form_field_option.status = FORM_FIELD_OPTION_STATUS[0][0]
            form_field_option.save()

    # Bulk Create - Option
    field_option_objects = []

    for option in options_to_create:
        field_option = FormFieldOption(
                            label = option['label'],
                            option_order = option['order'],
                            form_field = field_instance
                        )
        field_option_objects.append(field_option)

    FormFieldOption.objects.bulk_create(field_option_objects)

def get_field_option_values(option_ids = []):
    """
   Get Field Option Values - If option is non deleted
    """
    option_values = []

    field_options = FormFieldOption.objects.filter(id__in=option_ids).filter(status=FORM_FIELD_OPTION_STATUS[1][0])

    if field_options:
        for field_option in field_options:
            option_values.append(field_option.label)

    return option_values

def get_field_option_value(option_id = ""):
    """
   Get Field Option Value - If option is non deleted
    """
    option_value = ""

    if not option_id:
        field_option = FormFieldOption.objects.filter(id=option_id).filter(status=FORM_FIELD_OPTION_STATUS[1][0]).first()

        if field_option:
            option_value = field_option.label

    return option_value