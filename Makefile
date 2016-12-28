clean:
	rm competition/scoring_program.zip
	rm competition/dev_data.zip
	rm competition/test_data.zip
	rm competition.zip

competition.zip:
	zip -j competition/scoring_program.zip scoring_program/*
	zip -j competition/dev_data.zip dev_data/*
	zip -j competition/test_data.zip test_data/*
	zip -j competition.zip competition/*

submission.zip:
	cd submission && zip ../submission.zip * && cd ..
