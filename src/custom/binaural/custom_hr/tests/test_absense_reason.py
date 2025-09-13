from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestHrAbsenceReason(TransactionCase):

    def setUp(self):
        super().setUp()
        # Create a test employee
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })

        # Create a hr leave type for hr.leave
        self.leave_type = self.env['hr.leave.type'].create({
            'name': 'Test Leave Type',
            'requires_allocation': 'no',
            
        })

    def test_create_absence_reason_success(self):
        # Test creating a valid absence reason
        reason = self.env['hr.absence.reason'].create({
            'name': 'Sickness',
            'code': 'TSICK', 
            'description': 'Absence due to illness'
        })
        self.assertTrue(reason.id)
        self.assertEqual(reason.name, 'Sickness')
        self.assertEqual(reason.code, 'TSICK')
        self.assertTrue(reason.active)

    def test_create_absence_reason_code_validation(self):
        # Test that code must be uppercase and contain no spaces
        with self.assertRaises(ValidationError):
            self.env['hr.absence.reason'].create({
                'name': 'Vacation',
                'code': 'vac1', 
            })
        with self.assertRaises(ValidationError):
            self.env['hr.absence.reason'].create({
                'name': 'Personal',
                'code': 'PER SON',  
            })

    def test_assign_reason_to_leave(self):
        # Test assigning a reason to a leave (hr.leave)
        reason = self.env['hr.absence.reason'].create({
            'name': 'Sickness',
            'code': 'TLEAVE',
        })
        leave = self.env['hr.leave'].create({
            'name': 'Test Leave',
            'employee_id': self.employee.id,
            'holiday_status_id': self.leave_type.id,
            'absence_reason_id': reason.id,
            'request_date_from': '2025-09-12',
            'request_date_to': '2025-09-12',
        })
        self.assertEqual(leave.absence_reason_id.id, reason.id)
        self.assertEqual(leave.absence_reason_id.name, 'Sickness')

    def test_visualize_absence_reasons(self):
        # Test that absence reasons can be retrieved for visualization
        reason1 = self.env['hr.absence.reason'].create({
            'name': 'Sickness',
            'code': 'TVIS1',
        })
        reason2 = self.env['hr.absence.reason'].create({
            'name': 'Vacation',
            'code': 'TVIS2',
        })
        reasons = self.env['hr.absence.reason'].search([('code', 'in', ['TVIS1', 'TVIS2'])])

        self.assertIn(reason1, reasons)
        self.assertIn(reason2, reasons)
        self.assertEqual(len(reasons), 2)
