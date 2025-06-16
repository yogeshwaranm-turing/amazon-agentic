from .apply_payment_to_loan import ApplyPaymentToLoan
from .create_invoice_payment import CreateInvoicePayment
from .create_refund import CreateRefund
from .delete_invoice import DeleteInvoice
from .delete_refund import DeleteRefund
from .list_overdue_invoices import ListOverdueInvoices
from .list_refunds_by_reason import ListRefundsByReason
from .transfer_to_human_agents import TransferToHumanAgents
from .update_invoice_details import UpdateInvoiceDetails
from .update_refund_status import UpdateRefundStatus


ALL_TOOLS_INTERFACE_3 = [
    ApplyPaymentToLoan,
    CreateInvoicePayment,
    CreateRefund,
    DeleteInvoice,  
    DeleteRefund,
    ListOverdueInvoices,
    ListRefundsByReason,
    TransferToHumanAgents,
    UpdateInvoiceDetails,
    UpdateRefundStatus,
]
