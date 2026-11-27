BASE_URL="http://localhost:8000"
EMAIL="test@example.com"
PASSWORD="secrepassword"

echo "logueando como $EMAIL"

TOKEN=$(curl -s -X POST "$BASE_URL/login" \ 
    -H "Content-Type: application/json" \
    -d '{"email": "$EMAIL", "password": "$PASSWORD"}' \
    | jq -r '.token')


if [ "$TOKEN" == "null" ] || [ -z "$TOKEN" ]; then
    echo "Login fallo. No se pudo recivir el token"
    exit 1
fi


echo "token adquirido! leyendo algun usuario"


curl -s -X GET "$BASE_URL/usuarios/{1}" \
    -H "Authorization: Bearer $TOKEN" \
    | jq '.'

