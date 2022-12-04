package Data.api.Demo;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/ecuador/v2.0/request/data/json")
public class TestingApiPe {
	
	public static final String jsonSend = "/?tipoPersona=N&_=1666065662590";
	private String dataReturnJson;
	
	@GetMapping
	public String sendRequestJson(@RequestParam (value="cedula") String cedula) {
		try {
			if(cedula.length() == 10) {
				String sendUrl = String.format("https://srienlinea.sri.gob.ec/movil-servicios/api/v1.0/deudas/porIdentificacion/%s", cedula);
				HttpClient clientRequest = HttpClient.newHttpClient();
				HttpRequest requestJson = HttpRequest.newBuilder()
						.uri((URI.create(sendUrl+jsonSend)))
						.header("Content-Type", "application/json")
						.GET()
						.build();
				HttpResponse<String> response = clientRequest.send(requestJson, HttpResponse.BodyHandlers.ofString());
				dataReturnJson = response.body();
				
			}else {
				return "LA CEDULA NO ES VALIDA";
			}
			
		}catch(Exception e) {
			return "OCURRIO UN ERROR"+e;
			
		}
		return dataReturnJson;
		
	}
	

}
