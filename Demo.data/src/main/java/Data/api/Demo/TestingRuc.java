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
@RequestMapping("/peru/data/ruc/")
public class TestingRuc {
	
	
	public static final String URL_REQUEST = "https://consulta.api-peru.com/api/ruc/";
	private String jsonResponse;
	@GetMapping
	@RequestMapping
	public String requestApiRuc(@RequestParam (value="ruc") String rucVerify) {
		try {
			if(rucVerify.length() == 11) {
				HttpClient requestApi = HttpClient.newHttpClient();
				HttpRequest sendData = HttpRequest.newBuilder()
						.uri(URI.create(URL_REQUEST+rucVerify))
						.GET()
						.header("Content-Type", "application/json")
						.build();
				HttpResponse<String> responseUrl = requestApi.send(sendData, HttpResponse.BodyHandlers.ofString());
				jsonResponse = responseUrl.body();
				
			}else {
				return "EL RUC INGRESADO NO ES VALIDO";
			}
			
		}catch(Exception e) {
			return "OCURRIO UN ERROR "+e;
			
		}
		
		return jsonResponse;
	}

}
