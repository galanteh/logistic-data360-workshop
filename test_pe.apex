LOG_AlertaIncidencia__e evt = new LOG_AlertaIncidencia__e();
  evt.NumGuia__c          = 'SYNTH-TEST-001';
  evt.Key_Qualifier_Incident_Id__c = 'TEST-ID-001';
  evt.Internal_Organization__c     = 'Medicaltech';
  Database.SaveResult sr = EventBus.publish(evt);
  System.debug('Publicado: ' + sr.isSuccess() + ' | Errors: ' + sr.getErrors());
