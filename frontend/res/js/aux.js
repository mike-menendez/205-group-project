$.ajax({
    type: "POST",
    url: "http://rts.interviewhigh.com",
    data: {
        "uuid" : "mike",
        "input" : "1\n2\n", // the different test cases need to be seperated by \n
        "code" : "#include <iostream>\nusing namespace std;\n int main(){\n int i =0;\n cin >> i;\n cout << i+1 << endl;\nreturn 0;\n}}",
        "question_id" : "cst_205",
        "lang" : "cpp"
    }
})
