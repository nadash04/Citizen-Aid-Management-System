# create_initial_data.py - Script to populate initial data

import backend_functions as be
import datetime
import random

def create_initial_data():
    """Creates initial data for the system including admins, citizens, aid history, and messages."""
    
    print("Setting up CSV files...")
    be.setup_csv_files()
    
    print("Creating initial admin accounts...")
    
    # Create admin accounts
    admins_data = [
        {"username": "admin", "password": "admin123", "full_name": "System Administrator", "organization_id": "ORG001", "role": "admin"},
        {"username": "manager", "password": "manager123", "full_name": "Aid Manager", "organization_id": "ORG001", "role": "manager"},
        {"username": "supervisor", "password": "super123", "full_name": "Field Supervisor", "organization_id": "ORG002", "role": "supervisor"}
    ]
    
    for admin_data in admins_data:
        success = be.register_admin_csv(
            username=admin_data["username"],
            password=admin_data["password"],
            full_name=admin_data["full_name"],
            organization_id=admin_data["organization_id"],
            role=admin_data["role"]
        )
        if success:
            print(f"✓ Created admin: {admin_data['username']}")
        else:
            print(f"✗ Failed to create admin: {admin_data['username']}")
    
    print("\nCreating initial citizen accounts...")
    
    # Create citizen accounts with varying priority scores
    citizens_data = [
        {
            "national_id": "123456789",
            "full_name": "أحمد محمد علي",
            "phone_number": "0501234567",
            "secret_code": "ahmed123",
            "priority_score": 7.0,  # High priority
            "date_of_birth": "1985-03-15",
            "address": " رفح ، حي البرازيل ، شارع السلام ",
            "household_members": 6,
            "dependents": 4,
            "needs_description": "عائل أسرة من ذوي الاحتياجات الخاصة، يحتاج مساعدة عاجلة"
        },
        {
            "national_id": "234567890",
            "full_name": "فاطمة عبدالله أبو وردة",
            "phone_number": "0502345678",
            "secret_code": "fatima456",
            "priority_score": 5.0,  # Medium-high priority
            "date_of_birth": "1990-07-22",
            "address": "شمال غزة مخيم جباليا حي القصاصيب ",
            "household_members": 4,
            "dependents": 2,
            "needs_description": "أم عزباء مع طفلين، دخل محدود"
        },
        {
            "national_id": "345678901",
            "full_name": "خالد سعد الشنطي",
            "phone_number": "0503456789",
            "secret_code": "khalid789",
            "priority_score": 3.0,  # Medium priority
            "date_of_birth": "1978-12-10",
            "address": "مدينة غزة ، حي الرمال ، شار الكنز ",
            "household_members": 5,
            "dependents": 3,
            "needs_description": "عامل بناء، دخل غير منتظم"
        },
        {
            "national_id": "456789012",
            "full_name": "نورا إبراهيم أبوغالي",
            "phone_number": "0504567890",
            "secret_code": "nora2024",
            "priority_score": 6.0,  # High priority
            "date_of_birth": "1982-05-18",
            "address": "خانيونس حي الأمل ",
            "household_members": 7,
            "dependents": 5,
            "needs_description": "أسرة كبيرة، الأب مريض مزمن"
        },
        {
            "national_id": "567890123",
            "full_name": "محمد عبدالعزيز القطناني",
            "phone_number": "0505678901",
            "secret_code": "mohammed321",
            "priority_score": 2.0,  # Lower priority
            "date_of_birth": "1995-09-03",
            "address": "خانيونس ، بلدة القرارة",
            "household_members": 3,
            "dependents": 1,
            "needs_description": "خريج جامعي، يبحث عن عمل"
        },
        {
            "national_id": "678901234",
            "full_name": "سارة أحمد الشريف ",
            "phone_number": "0506789012",
            "secret_code": "sara2024",
            "priority_score": 4.0,  # Medium priority
            "date_of_birth": "1988-11-25",
            "address": "مدينة غزة ، حي التفاح شارع يافا",
            "household_members": 4,
            "dependents": 2,
            "needs_description": "معلمة، راتب محدود مع التزامات عائلية"
        },
        {
            "national_id": "789012345",
            "full_name": "عبدالرحمن فهد المصري",
            "phone_number": "0507890123",
            "secret_code": "abdulrahman",
            "priority_score": 1.0,  # Low priority
            "date_of_birth": "1992-01-14",
            "address": "غزة ، حي الكرامة ",
            "household_members": 2,
            "dependents": 0,
            "needs_description": "موظف حكومي، وضع مالي مستقر نسبياً"
        },
        {
            "national_id": "890123456",
            "full_name": "أفنان محمد أبو معمر ",
            "phone_number": "0508901234",
            "secret_code": "afnan123",
            "priority_score": 5.0,  # Medium-high priority
            "date_of_birth": "1987-04-08",
            "address":"غزة ، حي تل الهوى ",
            "household_members": 5,
            "dependents": 3,
            "needs_description": "أرملة مع ثلاثة أطفال، تحتاج دعم مالي"
        }
    ]
    
    citizen_ids = []
    for citizen_data in citizens_data:
        registered_record = be.register_citizen_csv(citizen_data)
        if registered_record:
            citizen_id = registered_record.get("id")
            citizen_ids.append(citizen_id)
            print(f"✓ Created citizen: {citizen_data['full_name']} (ID: {citizen_id})")
        else:
            print(f"✗ Failed to create citizen: {citizen_data['full_name']}")
    
    print(f"\nCreated {len(citizen_ids)} citizens successfully.")
    
    print("\nCreating aid history records...")
    
    # Create some aid history records
    aid_records = [
        # Some citizens have received aid
        {"citizen_id": citizen_ids[0], "entry_type": "FoodAid", "date": "2024-01-15", "next_date": ""},  # Received
        {"citizen_id": citizen_ids[1], "entry_type": "CashAid", "date": "2024-02-10", "next_date": ""},  # Received
        {"citizen_id": citizen_ids[3], "entry_type": "MedicalAid", "date": "2024-01-20", "next_date": ""},  # Received
        {"citizen_id": citizen_ids[7], "entry_type": "FoodAid", "date": "2024-02-05", "next_date": ""},  # Received
        
        # Some have scheduled future aid
        {"citizen_id": citizen_ids[2], "entry_type": "AdminEntry", "date": "2024-03-01", "next_date": "2024-04-01"},
        {"citizen_id": citizen_ids[4], "entry_type": "AdminEntry", "date": "2024-02-28", "next_date": "2024-03-30"},
        {"citizen_id": citizen_ids[5], "entry_type": "AdminEntry", "date": "2024-03-05", "next_date": "2024-04-05"},
    ]
    
    for record in aid_records:
        if record["citizen_id"]:  # Make sure citizen ID exists
            success = be.save_aid_history_entry(
                citizen_internal_id=record["citizen_id"],
                entry_type=record["entry_type"],
                date_str=record["date"],
                next_date_str=record["next_date"]
            )
            if success:
                status = "Received" if record["next_date"] == "" else f"Scheduled for {record['next_date']}"
                print(f"✓ Created aid record for citizen {record['citizen_id']}: {record['entry_type']} - {status}")
            else:
                print(f"✗ Failed to create aid record for citizen {record['citizen_id']}")
    
    print("\nCreating message records...")
    
    # Create some messages
    messages = [
        {"citizen_id": citizen_ids[0], "message": "تم استلام طلبكم للمساعدة الغذائية. سيتم التواصل معكم قريباً."},
        {"citizen_id": citizen_ids[1], "message": "تم الموافقة على طلب المساعدة المالية. يرجى مراجعة المكتب لاستلام المبلغ."},
        {"citizen_id": citizen_ids[2], "message": "نأسف لتأخير الرد. طلبكم قيد المراجعة وسيتم الرد خلال أسبوع."},
        {"citizen_id": citizen_ids[3], "message": "تم ترتيب موعد للفحص الطبي يوم الأحد القادم في المستشفى العام."},
        {"citizen_id": citizen_ids[4], "message": "يرجى تحديث بياناتكم الشخصية في أقرب وقت ممكن."},
        {"citizen_id": citizen_ids[5], "message": "تم تسجيل طلبكم بنجاح. رقم الطلب: REQ-2024-001"},
        {"citizen_id": citizen_ids[6], "message": "شكراً لكم على التواصل. سيتم مراجعة حالتكم والرد قريباً."},
        {"citizen_id": citizen_ids[7], "message": "تم توزيع المساعدات الغذائية. يرجى استلامها من نقطة التوزيع المحددة."},
    ]
    
    for msg in messages:
        if msg["citizen_id"]:  # Make sure citizen ID exists
            success = be.save_message_entry(
                citizen_internal_id=msg["citizen_id"],
                message=msg["message"]
            )
            if success:
                print(f"✓ Created message for citizen {msg['citizen_id']}")
            else:
                print(f"✗ Failed to create message for citizen {msg['citizen_id']}")
    
    print("\n" + "="*60)
    print("INITIAL DATA CREATION COMPLETED!")
    print("="*60)
    print("\nAdmin Accounts Created:")
    print("Username: admin, Password: admin123")
    print("Username: manager, Password: manager123") 
    print("Username: supervisor, Password: super123")
    
    print(f"\nCitizen Accounts Created: {len(citizen_ids)}")
    print("Sample Citizen Login:")
    print("National ID: 123456789, Secret Code: ahmed123")
    print("National ID: 234567890, Secret Code: fatima456")
    print("National ID: 456789012, Secret Code: nora2024")
    
    print(f"\nAid Records Created: {len(aid_records)}")
    print(f"Messages Created: {len(messages)}")
    
    print("\nThe system is now ready for testing!")
    print("="*60)

if __name__ == "__main__":
    create_initial_data()

