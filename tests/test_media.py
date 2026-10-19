import hashlib, importlib.util, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('studio',ROOT/'tools/media_studio.py'); studio=importlib.util.module_from_spec(spec); spec.loader.exec_module(studio)
class ValidationTests(unittest.TestCase):
    def job(self):
        return {'job_id':'safe','approved':True,'script_text':'Owned source','script_sha256':hashlib.sha256(b'Owned source').hexdigest(),'scenes':[{'title':'Start','body':'A simple useful step.'}]}
    def test_valid_owned_job(self): self.assertIsNone(studio.validate(self.job()))
    def test_bad_input_is_rejected(self):
        for change in [{'approved':False},{'job_id':'../escape'},{'script_sha256':'0'*64},{'seconds_per_scene':100},{'narration_file':'../../secret.wav'},{'scenes':[{'title':'x','body':'x'*181}]}]:
            with self.subTest(change=change), self.assertRaises(ValueError): studio.validate({**self.job(),**change})
if __name__=='__main__': unittest.main()
