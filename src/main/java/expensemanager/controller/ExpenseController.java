package expensemanager.controller;

import expensemanager.entity.Expense;
import expensemanager.repository.ExpenseRepository;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.multipart.MultipartFile;

import com.itextpdf.text.Document;
import com.itextpdf.text.Paragraph;
import com.itextpdf.text.pdf.PdfPTable;
import com.itextpdf.text.pdf.PdfWriter;

import java.io.ByteArrayOutputStream;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;

import java.time.LocalDate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
@RestController
@CrossOrigin("*")
public class ExpenseController {

    @Autowired
    private ExpenseRepository expenseRepository;

    @PostMapping("/expenses")
    public Map<String,String> addExpense(
            @RequestBody Expense expense){

        expenseRepository.save(expense);

        Map<String,String> response =
                new HashMap<>();

        response.put(
                "message",
                "Expense added!");

        return response;
    }

    @GetMapping("/expenses/{userId}")
    public List<Expense> getExpenses(
            @PathVariable Long userId){

        return expenseRepository
                .findByUserId(userId);
    }

    @DeleteMapping("/expenses/{userId}/{expenseId}")
    public Map<String,String> deleteExpense(
            @PathVariable Long userId,
            @PathVariable Long expenseId){

        expenseRepository.deleteById(
                expenseId);

        Map<String,String> response =
                new HashMap<>();

        response.put(
                "message",
                "Deleted!");

        return response;
    }
    @GetMapping("/expenses/total/{userId}")
public Map<String, Double> getTotalExpense(
        @PathVariable Long userId) {

java.util.List<Expense> expenses =
        expenseRepository.findByUserId(userId);

    double total =
            expenses.stream()
                    .mapToDouble(
                            Expense::getAmount
                    )
                    .sum();

    Map<String, Double> response =
            new HashMap<>();

    response.put("total", total);

    return response;
}
@PostMapping("/expenses/total_between/{userId}")
public Map<String, Double> totalBetweenDates(
        @PathVariable Long userId,
        @RequestBody Map<String,String> body){

    LocalDate start =
            LocalDate.parse(
                    body.get("start")
            );

    LocalDate end =
            LocalDate.parse(
                    body.get("end")
            );

    List<Expense> expenses =
            expenseRepository
                    .findByUserIdAndDateBetween(
                            userId,
                            start,
                            end
                    );

    double total =
            expenses.stream()
                    .mapToDouble(
                            Expense::getAmount
                    )
                    .sum();

    Map<String, Double> response =
            new HashMap<>();

    response.put("total", total);

    return response;
}
@GetMapping("/expenses/search/{userId}")
public List<Expense> searchExpense(
        @PathVariable Long userId,
        @RequestParam String keyword){

    return expenseRepository
            .findByUserIdAndDescriptionContainingIgnoreCase(
                    userId,
                    keyword
            );
}
@PutMapping("/expenses/{id}")
public Expense editExpense(
        @PathVariable Long id,
        @RequestBody Expense updated){

    Expense expense =
            expenseRepository
                    .findById(id)
                    .orElseThrow();

    expense.setAmount(
            updated.getAmount()
    );

    expense.setDescription(
            updated.getDescription()
    );

    expense.setCategory(
            updated.getCategory()
    );

    expense.setDate(
            updated.getDate()
    );

    return expenseRepository.save(
            expense
    );
}
@GetMapping("/monthly_summary/{userId}")
public Map<String, Double> monthlySummary(
        @PathVariable Long userId) {

    List<Expense> expenses =
            expenseRepository.findByUserId(userId);

    Map<String, Double> result =
            new HashMap<>();

    for (Expense e : expenses) {

        String month =
                e.getDate()
                 .getMonth()
                 .toString();

        result.put(
                month,
                result.getOrDefault(month, 0.0)
                        + e.getAmount()
        );
    }

    return result;
}
@GetMapping("/yearly_summary/{userId}")
public Map<Integer, Double> yearlySummary(
        @PathVariable Long userId) {

    List<Expense> expenses =
            expenseRepository.findByUserId(userId);

    Map<Integer, Double> result =
            new HashMap<>();

    for (Expense e : expenses) {

        Integer year =
                e.getDate().getYear();

        result.put(
                year,
                result.getOrDefault(year, 0.0)
                        + e.getAmount()
        );
    }

    return result;
}
@GetMapping("/export_csv/{userId}")
public ResponseEntity<byte[]> exportCSV(
        @PathVariable Long userId) {

    List<Expense> expenses =
            expenseRepository.findByUserId(userId);

    ByteArrayOutputStream out =
            new ByteArrayOutputStream();

    PrintWriter writer =
            new PrintWriter(out);

    writer.println(
            "Date,Description,Amount,Category"
    );

    for (Expense e : expenses) {

        writer.println(
                e.getDate() + "," +
                e.getDescription() + "," +
                e.getAmount() + "," +
                e.getCategory()
        );
    }

    writer.flush();

    return ResponseEntity.ok()
            .header(
                    HttpHeaders.CONTENT_DISPOSITION,
                    "attachment; filename=expenses.csv"
            )
            .contentType(
                    MediaType.parseMediaType(
                            "text/csv"
                    )
            )
            .body(
                    out.toByteArray()
            );
}
@PostMapping("/import_csv")
public Map<String,String> importCSV(
        @RequestParam("file") MultipartFile file,
        @RequestParam Long userId) {

    Map<String,String> response =
            new HashMap<>();

    try {

        BufferedReader reader =
                new BufferedReader(
                        new InputStreamReader(
                                file.getInputStream()
                        )
                );

        String line;

        reader.readLine();

        while((line = reader.readLine()) != null){

            String[] data =
                    line.split(",");

            Expense expense =
                    new Expense();

            expense.setUserId(userId);

            expense.setDate(
                    LocalDate.parse(
                            data[0]
                    )
            );

            expense.setDescription(
                    data[1]
            );

            expense.setAmount(
                    Double.parseDouble(
                            data[2]
                    )
            );

            expense.setCategory(
                    data[3]
            );

            expenseRepository.save(
                    expense
            );
        }

        response.put(
                "message",
                "CSV imported successfully"
        );

    } catch(Exception e){

        response.put(
                "message",
                "Import failed"
        );
    }

    return response;
}
@GetMapping("/pdf_report/{userId}")
public ResponseEntity<byte[]> generatePDF(
        @PathVariable Long userId)
        throws Exception {

    List<Expense> expenses =
            expenseRepository.findByUserId(userId);

    Document document =
            new Document();

    ByteArrayOutputStream out =
            new ByteArrayOutputStream();

    PdfWriter.getInstance(
            document,
            out
    );

    document.open();

    document.add(
            new Paragraph(
                    "Expense Report"
            )
    );

    document.add(
            new Paragraph(" ")
    );

    PdfPTable table =
            new PdfPTable(4);

    table.addCell("Date");
    table.addCell("Description");
    table.addCell("Amount");
    table.addCell("Category");

    for(Expense e : expenses){

        table.addCell(
                e.getDate().toString()
        );

        table.addCell(
                e.getDescription()
        );

        table.addCell(
                e.getAmount().toString()
        );

        table.addCell(
                e.getCategory()
        );
    }

    document.add(table);

    document.close();

    return ResponseEntity.ok()
            .header(
                    HttpHeaders.CONTENT_DISPOSITION,
                    "attachment; filename=report.pdf"
            )
            .contentType(
                    MediaType.APPLICATION_PDF
            )
            .body(
                    out.toByteArray()
            );
}
@GetMapping("/category_summary/{userId}")
public Map<String, Double> categorySummary(
        @PathVariable Long userId){

    List<Expense> expenses =
            expenseRepository.findByUserId(userId);

    Map<String, Double> result =
            new HashMap<>();

    for(Expense e : expenses){

        result.put(
                e.getCategory(),
                result.getOrDefault(
                        e.getCategory(),
                        0.0
                ) + e.getAmount()
        );
    }

    return result;
}
}