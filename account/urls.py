
from django.urls import path
from .import views

urlpatterns = [
    path("account_create/",views.account_create,name="account_create"),
    path("account_details/",views.account_details,name="account_details"),
    path("account_update/<int:id>/",views.account_update,name="account_update"),
    path("Account_deleted/<int:id>/",views.Account_deleted,name="Account_deleted"),
    path("account_list/",views.account_list,name="account_list"),

    path("journal_create/",views.journal_create,name="journal_create"),
    path("journal_details/",views.journal_details,name="journal_details"),
    path("journal_update/<int:id>/",views.journal_update,name="journal_update"),
    path("journal_delete/<int:id>/",views.journal_delete,name="journal_delete"),
    path("journal_export/",views.journal_export,name="journal_export"),
    path("journal_list/",views.journal_list,name="journal_list"),


    path("journalentry_create/",views.journalentry_create,name="journalentry_create"),
    path("journal_entry_details/",views.journal_entry_details,name="journal_details"),
    path("journalentry_list/",views.journalentry_details,name="journalentry_details"),
    path("journal_entry_delete/<int:id>/",views.journal_entry_delete,name="journal_entry_delete"),


    path("journal_items_deleted/<int:id>/",views.journal_items),
    path("journal_items_details/",views.journal_items_details),
    path("JournalItems_list/",views.JournalItems_detail),


    path("trial_balance_view/",views.trial_balance_view,name="trial_balance"),
    path("genaral_ledger/<int:id>/",views.genaral_ledger,name="genaral_ledger"),







    path("customer/",views.create_customer,name="customer_create"),
    path("customer_details/",views.customer_details,name="customer_details"),
    path("customer_delete/<str:name>/",views.customer_delete,name="customer_delete"),
    path("customer_update/<str:email>/",views.customer_update,name="customer_update"),
    path("customer_export/",views.customer_export,name="customer_export"),
    path("customers_list/",views.customers_list,name="customers_list"),
    
    path("create_customercontact/",views.create_customercontact,name="create_customercontact"),
    path("contact_details/",views.contact_details,name="contact_details"),
    path("contact_delete/",views.contact_delete,name="contact_delete"),
    path("contact_update/<int:id>/",views.contact_update,name="contact_update"),

    path("product_create/",views.product_create ,name="product_create "),
    path("product_view/",views.product_view,name="product_view"),
    path("product_update/<str:name>/",views.product_update,name="product_update"),
    path("product_delete/<str:name>/",views.product_delete,name="product_delete"),

    path("invoice_create/",views.invoice_create,name="invoice_create"),
    path("invoice_list/",views.invoice_list,name="invoice_list"),
    path("customer_invoice_details/",views.invoice_details,name="invoice_details"),
    path("invoice_update/<int:id>/",views.invoice_update,name="invoice_update"),
    path("invoice_delete/<int:id>/",views.invoice_delete,name="invoice_delete"),
    path("payment_create/",views.payment_create,name="payment_create"),
    path("payment_update/<int:id>/",views.payment_update,name="payment_update"),
    path("payment_delete/<int:id>/",views.payment_delete,name="payment_delete"),



    path("vendor_create/",views.vendor_create,name="vendor_create"),
    path("vendor_details/",views.vendor_details,name="vendor_details"),
    path("vendor_update/<str:email>/",views.vendor_update,name="vendor_update"),
    path("vendor_delete/<str:name>/",views.vendor_delete,name="vendor_delete"),

    path("vendor_product_create/",views.vendor_product_create,name="vendor_product_create"),
    path("product_view_vendor/",views.vendor_product_view,name="product_view"),
    path("vendor_product_update/<int:id>/",views.vendor_product_update,name="vendor_product_update"),
    path("vendor_product_delete/<int:id>/",views.vendor_product_delete,name="vendor_product_delete"),

    path("vendor_invoice_create/",views.vendor_invoice_create,name="vendor_invoice_create"),
    path("vendor_invoice_display/",views.vendor_invoice_display,name="vendor_invoice_display"),
    path("vendorinvoice_delete/",views.vendorinvoice_delete,name="vendorinvoice_delete"),

    
    path("vendor_payment_create/",views.vendor_payment_create,name="vendor_payment_create"),
    path("vendor_payment_details/",views.vendor_payment_details,name="vendor_payment_details"),
    path("vendor_payment_delete/",views.vendor_payment_delete,name="vendor_payment_delete"),

    path("total_revenue/",views.total_revenue,name="total_revenue"),
    path("total_Expense/",views.total_Expense,name="total_Expense"),
    path("total_customers/",views.total_Customers,name="total_customers"),
    path("total_vendors/",views.total_Vendors,name="total_vendors"),
    path("recent_invoices/",views.recent_invoices,name="recent_invoices"),
    path("recent_payments/",views.recent_payments,name="recent_payments"),
    path("recent_vendor_invoices/",views.recent_vendor_invoices,name="recent_vendor_invoices"),
    path("recent_vendor_payments/",views.recent_vendor_payments,name="recent_vendor_payments"),



    
]