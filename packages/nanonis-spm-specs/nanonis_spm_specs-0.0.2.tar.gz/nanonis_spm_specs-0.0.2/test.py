import nanonis_spm_specs


nanonisInstance = nanonis_spm_specs.Nanonis(6501, '10.0.0.37')


#TEST COMMAND
nanonisInstance.DataLog_Open()
