from django.shortcuts import render

# home action for calculator 
def home(request):
	key = request.POST.get("key") or None
	first = ""
	second = ""
	op = ""
	if key != None and ":" in key:
		arr = key.split(":")
		key = arr[0]
		first = arr[1]
		second = arr[2]
		op = arr[3]
	
	context = {}
	if(key != None):
		key = key.replace("Error","")
		prev = key[:-1]
		last = key[-1]
		print("case...", "key:",key, "op:",op, "first:",first,"second:",second,"last:", last)
		
		if((key == last) and containsOps(last) and key[0] != "-" and first == ""):
			print("case0 when input starts with operator except(-) -> avoid it")
			key = prev
			context["key"] = key
			context["first"] = first
		elif((isValidOp(op) and first != "" and containsOps(last) and second == "") or (len(key) > 1 and (isValidOp(key[-1]) and isValidOp(key[-2])))):
			print("case1 when same or diff operators repeats one after another")
			key = prev
			if(key[0] == "-" and containsOps(last) and first == ""):
				key = ""
				context["key"] = key
				context["first"] = first
				context["op"] = ""
				context["second"] = second

			else:
				prev = key[:-1]
				context["key"] = key
				context["first"] = first
				context["op"] = last
				context["second"] = second

		elif((last == "=" and first == "" and isEmptyOp(op)) or (first != "" and second == "" and isValidOp(op) and last == "=")):
			print("case2")
			key = prev
			prev = key[:-1]
			context["key"] = key
			context["op"] = op
			context["first"] = first

		elif(last == "=" and first != "" and isValidOp(op) and second != ""):
			print("case3 - on press equal")
			key = exec_op(key, first, second,  op)
			if(key == None):
				context["key"] = "Error"
			else:	
				context["key"] = key
			context["first"] = ""
			context["second"] = ""
			context["op"] = "=" #"="
		elif(last == "+" or (len(key) > 1 and last == "-") or last == "*" or last == "/"):
			print("on operator found")
			if(first == "" and isEmptyOp(op)):
				print("case4-1 first op")
				op = last
				first = prev
				context["op"] = op
				context["first"] = first
				context["key"] = first
			elif(second == "" and last == "-"):
				print("case4-2")
				context["key"] = last
				context["second"] = last
				context["op"] = op
				context["first"] = first

			else:
				print("case4-3 on 2nd op found")
				key = exec_op(key, first, second, op)
				if(key == None):
					context["key"] = "Error"
					context["first"] = ""
					context["op"] = ""
				else:
					context["key"] = key
					context["first"] = key
					context["op"] = last
		else:
			if(op == "=" and first == "" and second == ""):
				print("case5-0")
				op = ""
				context["op"] = op
				context["key"] = last
			elif(first != "" and isValidOp(op) and second == ""):
				print("case5-1 start second param")
				context["key"] = last
				context["second"] = last
			else:
				print("case5-2 append")
				context["key"] = key
				if(second != ""):
					context["second"] = key
			context["op"] = op
			context["first"] = first
	else:
		print("case6")
		context["op"] = op
		context["first"] = first
		context["key"] = ""
	
	return render(request, "calculator.html", context)

def isEmptyOp(key):
	return (key == "" or key == "=")

def isValidOp(key):
	return (key == "+" or key == "-" or key == "*" or key == "/")

def containsOps(key):
	return ("+" in key or ("-" in key) or "*" in key or "/" in key) 
	#return ("+" in key or ("-" in key[1:]) or "*" in key or "/" in key) 

def exec_op(key, first, second, op):
	if op == "+":
		pre = int(first) + int(second)
		key = str(pre)
	elif op == "-":
		pre = int(first) - int(second)
		key = str(pre)
	elif op == "*":
		pre = int(first) * int(second)
		key = str(pre)
	elif op == "/":
		if int(second) != 0:
			pre = int(first) / int(second)
			key = str(pre)
		else:
			key = None
	return key

