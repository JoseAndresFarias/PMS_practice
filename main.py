from datetime import datetime

from models import Building, Lease, Resident, Unit
from repositories import (
    BuildingRepository,
    LeaseRepository,
    ResidentRepository,
    UnitRepository,
)

building_repo = BuildingRepository()
unit_repo = UnitRepository()
resident_repo = ResidentRepository()
lease_repo = LeaseRepository()


def print_section(title: str) -> None:
    print(f"\n{'=' * 40}")
    print(f"  {title}")
    print('=' * 40)


def main() -> None:
    # --- Buildings ---
    print_section("Creating Buildings")
    b1 = Building(name="Sunset Apartments", address="123 Main St", city="Austin", state="TX", zip_code="78701")
    b2 = Building(name="Oak Tower", address="456 Elm Ave", city="Austin", state="TX", zip_code="78702")
    building_repo.save(b1)
    building_repo.save(b2)
    print(f"Saved: {b1.name} (id={b1.id})")
    print(f"Saved: {b2.name} (id={b2.id})")

    # --- Units ---
    print_section("Creating Units")
    u1 = Unit(building_id=b1.id, unit_number="101", bedrooms=1, bathrooms=1.0, rent_amount=1200.0)
    u2 = Unit(building_id=b1.id, unit_number="102", bedrooms=2, bathrooms=1.0, rent_amount=1500.0)
    u3 = Unit(building_id=b2.id, unit_number="201", bedrooms=3, bathrooms=2.0, rent_amount=2200.0)
    for unit in (u1, u2, u3):
        unit_repo.save(unit)
        print(f"Saved: Unit {unit.unit_number} in building {unit.building_id} — ${unit.rent_amount}/mo")

    # --- Residents ---
    print_section("Creating Residents")
    r1 = Resident(first_name="Jane", last_name="Doe", email="jane@example.com", phone="555-0101")
    r2 = Resident(first_name="John", last_name="Smith", email="john@example.com", phone="555-0202")
    for resident in (r1, r2):
        resident_repo.save(resident)
        print(f"Saved: {resident.first_name} {resident.last_name} ({resident.email})")

    # --- Leases ---
    print_section("Creating Leases")
    l1 = Lease(
        unit_id=u1.id,
        resident_id=r1.id,
        start_date=datetime(2026, 1, 1),
        end_date=datetime(2026, 12, 31),
        monthly_rent=1200.0,
    )
    l2 = Lease(
        unit_id=u2.id,
        resident_id=r2.id,
        start_date=datetime(2026, 3, 1),
        end_date=datetime(2027, 2, 28),
        monthly_rent=1500.0,
    )
    for lease in (l1, l2):
        lease_repo.save(lease)
        print(f"Saved: Lease {lease.id} — unit {lease.unit_id} / resident {lease.resident_id} [{lease.status}]")

    # --- Reload from disk ---
    print_section("Reloading from Disk")
    all_buildings = building_repo.get_all()
    all_units = unit_repo.get_all()
    all_residents = resident_repo.get_all()
    all_leases = lease_repo.get_all()
    print(f"Buildings : {len(all_buildings)}")
    print(f"Units     : {len(all_units)}")
    print(f"Residents : {len(all_residents)}")
    print(f"Leases    : {len(all_leases)}")

    # --- Archive a lease ---
    print_section("Archiving a Lease")
    l1.archive()
    lease_repo.save(l1)
    print(f"Lease {l1.id} archived at {l1.archived_at}")

    active_leases = lease_repo.get_active()
    print(f"Active leases after archive: {len(active_leases)}")
    for lease in active_leases:
        print(f"  - Lease {lease.id} [{lease.status}]")

    # --- get_by_id ---
    print_section("Fetching by ID")
    fetched = building_repo.get_by_id(b1.id)
    print(f"Fetched building: {fetched.name}, {fetched.address}, {fetched.city}")

    missing = building_repo.get_by_id(__import__('uuid').uuid4())
    print(f"Non-existent ID returns: {missing}")


if __name__ == "__main__":
    main()
