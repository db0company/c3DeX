from magi.forms import (
    AccountForm as _AccountForm,
)

############################################################
# Account = attended ccc
############################################################

class AccountForm(_AccountForm):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        if not self.is_creating and 'ccc' in self.fields:
            del(self.fields['ccc'])

    class Meta(_AccountForm.Meta):
        allow_initial_in_get = ['ccc']
        exclude_fields = ['level', 'start_date', 'nickname']
