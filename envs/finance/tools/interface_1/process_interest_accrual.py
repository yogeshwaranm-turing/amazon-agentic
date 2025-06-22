import json
from typing import Any, Dict
from datetime import datetime, timedelta
from tau_bench.envs.tool import Tool

class ProcessInterestAccrual(Tool):
    @staticmethod
    def invoke(
        data: Dict[str, Any],
        account_id: str = None,
        process_all: bool = False
    ) -> str:
        accounts = data.get("accounts", {})
        
        if not process_all and not account_id:
            raise ValueError("Must specify either account_id or set process_all=True")
        
        processed_accounts = []
        
        # Determine which accounts to process
        if process_all:
            target_accounts = {aid: acc for aid, acc in accounts.items() 
                             if acc.get("account_type") == "savings" and acc.get("status") == "open"}
        else:
            if account_id not in accounts:
                raise ValueError(f"Account {account_id} not found.")
            target_accounts = {account_id: accounts[account_id]}
        
        for acc_id, account in target_accounts.items():
            # Only process savings accounts that are open
            if account.get("account_type") != "savings" or account.get("status") != "open":
                continue
            
            # Get account details
            balance = account.get("balances", {}).get("book", 0)
            annual_rate = account.get("interest_rate", 0) / 100
            last_posted = account.get("last_interest_posted")
            
            # Calculate interest (daily compounding)
            days_since_last_post = 30  # Default to monthly
            if last_posted:
                try:
                    last_date = datetime.fromisoformat(last_posted.replace("Z", ""))
                    days_since_last_post = (datetime.now() - last_date).days
                except:
                    days_since_last_post = 30
            
            # Calculate compound interest
            daily_rate = annual_rate / 365
            interest_earned = balance * ((1 + daily_rate) ** days_since_last_post - 1)
            
            # Update account
            new_accrued = account.get("interest_accrued", 0) + interest_earned
            new_balance = balance + interest_earned
            
            account["interest_accrued"] = round(new_accrued, 2)
            account["balances"]["book"] = round(new_balance, 2)
            account["balances"]["available"] = round(new_balance, 2)
            account["last_interest_posted"] = datetime.now().isoformat() + "Z"
            account["last_interest_amount"] = round(interest_earned, 2)
            
            processed_accounts.append({
                "account_id": acc_id,
                "interest_earned": round(interest_earned, 2),
                "new_balance": round(new_balance, 2),
                "total_accrued": round(new_accrued, 2)
            })
        
        return json.dumps({
            "processed_accounts": processed_accounts,
            "total_accounts": len(processed_accounts),
            "processing_date": datetime.now().isoformat() + "Z"
        })

    @staticmethod
    def get_info() -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "process_interest_accrual",
                "description": "Calculate and post interest to savings accounts, updating interest_accrued and balances.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "account_id": {"type": "string"},
                        "process_all": {"type": "boolean"}
                    },
                    "required": []
                }
            }
        }
